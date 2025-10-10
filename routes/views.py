from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.db import transaction
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
import logging
import csv
from datetime import datetime
from django.http import HttpResponse
from .models import Route, AdminUser
from .serializers import RouteSerializer
# from .google_sheets import RoutesGoogleSheetsSync  # Отключено, используем SQLite

logger = logging.getLogger(__name__)


class RouteListCreateView(generics.ListCreateAPIView):
    """Представление для получения списка трасс и создания новой трассы"""
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get_queryset(self):
        """Фильтрация трасс по параметрам запроса"""
        try:
            queryset = Route.objects.all()
            
            # Фильтр по сложности
            difficulty = self.request.query_params.get('difficulty', None)
            if difficulty:
                if difficulty not in [choice[0] for choice in Route.DifficultyLevel.choices]:
                    logger.warning(f"Некорректный уровень сложности: {difficulty}")
                    return Route.objects.none()
                queryset = queryset.filter(difficulty=difficulty)
            
            # Фильтр по автору
            author = self.request.query_params.get('author', None)
            if author:
                queryset = queryset.filter(author__icontains=author)
            
            # Фильтр по цвету
            color = self.request.query_params.get('color', None)
            if color:
                queryset = queryset.filter(color__icontains=color)
            
            # Фильтр по активности
            is_active = self.request.query_params.get('is_active', None)
            if is_active is not None:
                queryset = queryset.filter(is_active=is_active.lower() == 'true')
            
            # Поиск по названию
            search = self.request.query_params.get('search', None)
            if search:
                queryset = queryset.filter(name__icontains=search)
            
            logger.info(f"Выполнен поиск трасс с параметрами: {self.request.query_params}")
            return queryset
            
        except Exception as e:
            logger.error(f"Ошибка при получении списка трасс: {str(e)}")
            return Route.objects.none()

    def create(self, request, *args, **kwargs):
        """Создание новой трассы с логированием"""
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                route = serializer.save()
                logger.info(f"Создана новая трасса: {route.name} (ID: {route.id})")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.warning(f"Ошибка валидации при создании трассы: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Ошибка при создании трассы: {str(e)}")
            return Response(
                {'error': 'Внутренняя ошибка сервера'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RouteDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Представление для получения, обновления и удаления конкретной трассы"""
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def retrieve(self, request, *args, **kwargs):
        """Получение конкретной трассы с логированием"""
        try:
            instance = self.get_object()
            logger.info(f"Запрошена трасса: {instance.name} (ID: {instance.id})")
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Route.DoesNotExist:
            logger.warning(f"Трасса с ID {kwargs.get('pk')} не найдена")
            return Response(
                {'error': 'Трасса не найдена'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Ошибка при получении трассы: {str(e)}")
            return Response(
                {'error': 'Внутренняя ошибка сервера'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, *args, **kwargs):
        """Обновление трассы с логированием"""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
            if serializer.is_valid():
                try:
                    route = serializer.save()
                except ValidationError as ve:
                    logger.warning(f"Ошибка валидации модели при обновлении трассы: {ve.message_dict if hasattr(ve, 'message_dict') else str(ve)}")
                    return Response(getattr(ve, 'message_dict', {'__all__': [str(ve)]}), status=status.HTTP_400_BAD_REQUEST)
                logger.info(f"Обновлена трасса: {route.name} (ID: {route.id})")
                return Response(serializer.data)
            else:
                logger.warning(f"Ошибка валидации при обновлении трассы: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Route.DoesNotExist:
            logger.warning(f"Трасса с ID {kwargs.get('pk')} не найдена")
            return Response(
                {'error': 'Трасса не найдена'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except ValidationError as ve:
            logger.warning(f"Ошибка валидации модели при обновлении трассы (внешний catch): {ve}")
            return Response(getattr(ve, 'message_dict', {'__all__': [str(ve)]}), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Ошибка при обновлении трассы: {str(e)}")
            return Response(
                {'error': 'Внутренняя ошибка сервера'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, *args, **kwargs):
        """Удаление трассы с логированием"""
        try:
            instance = self.get_object()
            route_name = instance.name
            route_id = instance.id
            instance.delete()
            
            # Перенумеровываем оставшиеся трассы
            Route.renumber_routes()
            logger.info(f"Удалена трасса: {route_name} (ID: {route_id}) и выполнена перенумерация")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Route.DoesNotExist:
            logger.warning(f"Трасса с ID {kwargs.get('pk')} не найдена")
            return Response(
                {'error': 'Трасса не найдена'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Ошибка при удалении трассы: {str(e)}")
            return Response(
                {'error': 'Внутренняя ошибка сервера'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET'])
def difficulty_levels(request):
    """API endpoint для получения доступных уровней сложности"""
    levels = [
        {'value': choice[0], 'label': choice[1]} 
        for choice in Route.DifficultyLevel.choices
    ]
    return Response(levels)


@api_view(['GET'])
def route_stats(request):
    """API endpoint для получения статистики по трассам"""
    total_routes = Route.objects.count()
    active_routes = Route.objects.filter(is_active=True).count()
    
    difficulty_stats = {}
    for choice in Route.DifficultyLevel.choices:
        count = Route.objects.filter(difficulty=choice[0]).count()
        difficulty_stats[choice[0]] = {
            'label': choice[1],
            'count': count
        }
    
    color_stats = {}
    colors = Route.objects.values_list('color', flat=True).distinct()
    for color in colors:
        count = Route.objects.filter(color=color).count()
        color_stats[color] = count
    
    return Response({
        'total_routes': total_routes,
        'active_routes': active_routes,
        'inactive_routes': total_routes - active_routes,
        'difficulty_distribution': difficulty_stats,
        'color_distribution': color_stats
    })


class RouteBulkOperationsView(APIView):
    """Представление для массовых операций с трассами"""

    def post(self, request):
        """Массовое создание трасс"""
        try:
            routes_data = request.data.get('routes', [])
            if not routes_data:
                return Response(
                    {'error': 'Не предоставлены данные для создания трасс'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            created_routes = []
            errors = []

            with transaction.atomic():
                for i, route_data in enumerate(routes_data):
                    serializer = RouteSerializer(data=route_data)
                    if serializer.is_valid():
                        route = serializer.save()
                        created_routes.append(serializer.data)
                        logger.info(f"Создана трасса в массовой операции: {route.name} (ID: {route.id})")
                    else:
                        errors.append({
                            'index': i,
                            'data': route_data,
                            'errors': serializer.errors
                        })

            if errors:
                logger.warning(f"Ошибки при массовом создании трасс: {errors}")
                return Response({
                    'created_routes': created_routes,
                    'errors': errors,
                    'message': f'Создано {len(created_routes)} трасс, {len(errors)} ошибок'
                }, status=status.HTTP_207_MULTI_STATUS)
            else:
                logger.info(f"Успешно создано {len(created_routes)} трасс в массовой операции")
                return Response({
                    'created_routes': created_routes,
                    'message': f'Успешно создано {len(created_routes)} трасс'
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Ошибка при массовом создании трасс: {str(e)}")
            return Response(
                {'error': 'Внутренняя ошибка сервера'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request):
        """Массовое удаление трасс"""
        try:
            route_ids = request.data.get('route_ids', [])
            if not route_ids:
                return Response(
                    {'error': 'Не предоставлены ID трасс для удаления'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            deleted_count = 0
            not_found_ids = []

            with transaction.atomic():
                for route_id in route_ids:
                    try:
                        route = Route.objects.get(id=route_id)
                        route_name = route.name
                        route.delete()
                        deleted_count += 1
                        logger.info(f"Удалена трасса в массовой операции: {route_name} (ID: {route_id})")
                    except Route.DoesNotExist:
                        not_found_ids.append(route_id)
                        logger.warning(f"Трасса с ID {route_id} не найдена для массового удаления")

            # Перенумеровываем оставшиеся трассы
            if deleted_count > 0:
                Route.renumber_routes()
                logger.info(f"Выполнена перенумерация после удаления {deleted_count} трасс")

            response_data = {
                'deleted_count': deleted_count,
                'message': f'Удалено {deleted_count} трасс'
            }

            if not_found_ids:
                response_data['not_found_ids'] = not_found_ids
                response_data['message'] += f', {len(not_found_ids)} не найдено'

            logger.info(f"Массовое удаление завершено: удалено {deleted_count} трасс")
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Ошибка при массовом удалении трасс: {str(e)}")
            return Response(
                {'error': 'Внутренняя ошибка сервера'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['POST'])
def route_bulk_update(request):
    """Массовое обновление трасс"""
    try:
        updates_data = request.data.get('updates', [])
        if not updates_data:
            return Response(
                {'error': 'Не предоставлены данные для обновления трасс'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        updated_routes = []
        errors = []

        with transaction.atomic():
            for update_data in updates_data:
                route_id = update_data.get('id')
                if not route_id:
                    errors.append({
                        'data': update_data,
                        'error': 'Не указан ID трассы'
                    })
                    continue

                try:
                    route = Route.objects.get(id=route_id)
                    serializer = RouteSerializer(route, data=update_data, partial=True)
                    if serializer.is_valid():
                        updated_route = serializer.save()
                        updated_routes.append(serializer.data)
                        logger.info(f"Обновлена трасса в массовой операции: {updated_route.name} (ID: {route_id})")
                    else:
                        errors.append({
                            'id': route_id,
                            'data': update_data,
                            'errors': serializer.errors
                        })
                except Route.DoesNotExist:
                    errors.append({
                        'id': route_id,
                        'error': 'Трасса не найдена'
                    })

        if errors:
            logger.warning(f"Ошибки при массовом обновлении трасс: {errors}")
            return Response({
                'updated_routes': updated_routes,
                'errors': errors,
                'message': f'Обновлено {len(updated_routes)} трасс, {len(errors)} ошибок'
            }, status=status.HTTP_207_MULTI_STATUS)
        else:
            logger.info(f"Успешно обновлено {len(updated_routes)} трасс в массовой операции")
            return Response({
                'updated_routes': updated_routes,
                'message': f'Успешно обновлено {len(updated_routes)} трасс'
            }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Ошибка при массовом обновлении трасс: {str(e)}")
        return Response(
            {'error': 'Внутренняя ошибка сервера'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def route_search(request):
    """Расширенный поиск трасс с множественными критериями"""
    try:
        queryset = Route.objects.all()
        
        # Поиск по названию
        name = request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)
        
        # Поиск по автору
        author = request.query_params.get('author', None)
        if author:
            queryset = queryset.filter(author__icontains=author)
        
        # Фильтр по сложности
        difficulty = request.query_params.get('difficulty', None)
        if difficulty:
            if difficulty not in [choice[0] for choice in Route.DifficultyLevel.choices]:
                return Response(
                    {'error': f'Некорректный уровень сложности: {difficulty}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            queryset = queryset.filter(difficulty=difficulty)
        
        # Фильтр по цвету
        color = request.query_params.get('color', None)
        if color:
            queryset = queryset.filter(color__icontains=color)
        
        # Фильтр по активности
        is_active = request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Фильтр по дате создания (от)
        created_after = request.query_params.get('created_after', None)
        if created_after:
            try:
                from datetime import datetime
                date_obj = datetime.fromisoformat(created_after.replace('Z', '+00:00'))
                queryset = queryset.filter(created_at__gte=date_obj)
            except ValueError:
                return Response(
                    {'error': 'Некорректный формат даты для created_after'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Фильтр по дате создания (до)
        created_before = request.query_params.get('created_before', None)
        if created_before:
            try:
                from datetime import datetime
                date_obj = datetime.fromisoformat(created_before.replace('Z', '+00:00'))
                queryset = queryset.filter(created_at__lte=date_obj)
            except ValueError:
                return Response(
                    {'error': 'Некорректный формат даты для created_before'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Сортировка
        ordering = request.query_params.get('ordering', '-created_at')
        if ordering:
            allowed_fields = ['name', 'author', 'difficulty', 'created_at', '-name', '-author', '-difficulty', '-created_at']
            if ordering in allowed_fields:
                queryset = queryset.order_by(ordering)
        
        # Пагинация
        page_size = int(request.query_params.get('page_size', 20))
        page = int(request.query_params.get('page', 1))
        
        start = (page - 1) * page_size
        end = start + page_size
        
        total_count = queryset.count()
        routes = queryset[start:end]
        
        serializer = RouteSerializer(routes, many=True)
        
        logger.info(f"Выполнен расширенный поиск: найдено {total_count} трасс")
        
        return Response({
            'results': serializer.data,
            'count': total_count,
            'page': page,
            'page_size': page_size,
            'total_pages': (total_count + page_size - 1) // page_size
        })
        
    except Exception as e:
        logger.error(f"Ошибка при расширенном поиске: {str(e)}")
        return Response(
            {'error': 'Внутренняя ошибка сервера'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def route_authors(request):
    """Получить список всех авторов трасс"""
    try:
        authors = Route.objects.values_list('author', flat=True).distinct().order_by('author')
        author_stats = []
        
        for author in authors:
            route_count = Route.objects.filter(author=author).count()
            active_count = Route.objects.filter(author=author, is_active=True).count()
            author_stats.append({
                'name': author,
                'total_routes': route_count,
                'active_routes': active_count,
                'inactive_routes': route_count - active_count
            })
        
        logger.info(f"Запрошен список авторов: {len(author_stats)} авторов")
        return Response(author_stats)
        
    except Exception as e:
        logger.error(f"Ошибка при получении списка авторов: {str(e)}")
        return Response(
            {'error': 'Внутренняя ошибка сервера'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def route_colors(request):
    """Получить список всех цветов трасс"""
    try:
        colors = Route.objects.values_list('color', flat=True).distinct().order_by('color')
        color_stats = []
        
        for color in colors:
            route_count = Route.objects.filter(color=color).count()
            active_count = Route.objects.filter(color=color, is_active=True).count()
            color_stats.append({
                'name': color,
                'total_routes': route_count,
                'active_routes': active_count,
                'inactive_routes': route_count - active_count
            })
        
        logger.info(f"Запрошен список цветов: {len(color_stats)} цветов")
        return Response(color_stats)
        
    except Exception as e:
        logger.error(f"Ошибка при получении списка цветов: {str(e)}")
        return Response(
            {'error': 'Внутренняя ошибка сервера'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def route_toggle_active(request, pk):
    """Переключить статус активности трассы"""
    try:
        try:
            route = Route.objects.get(id=pk)
        except Route.DoesNotExist:
            return Response(
                {'error': 'Трасса не найдена'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        route.is_active = not route.is_active
        route.save()
        
        status_text = 'активна' if route.is_active else 'неактивна'
        logger.info(f"Изменен статус трассы {route.name} (ID: {pk}): {status_text}")
        
        serializer = RouteSerializer(route)
        return Response({
            'message': f'Трасса "{route.name}" теперь {status_text}',
            'route': serializer.data
        })
        
    except Exception as e:
        logger.error(f"Ошибка при переключении статуса трассы: {str(e)}")
        return Response(
            {'error': 'Внутренняя ошибка сервера'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def home_view(request):
    """Главная страница веб-приложения для управления API"""
    try:
        from datetime import datetime, timedelta
        
        # Получаем данные из SQLite базы данных
        all_routes = Route.objects.all().order_by('track_lane', 'route_number')
        active_routes = Route.objects.filter(is_active=True).order_by('track_lane', 'route_number')
        
        # Получаем текущую дату
        today = datetime.now().date()
        
        # Считаем новые трассы (младше 30 дней)
        new_routes = 0
        for route in active_routes:
            setup_date_str = route.setup_date
            if setup_date_str:
                try:
                    # Парсим дату в формате DD.MM.YYYY
                    setup_date = datetime.strptime(setup_date_str, '%d.%m.%Y').date()
                    if (today - setup_date).days <= 30:
                        new_routes += 1
                except ValueError:
                    # Если дата в неправильном формате, пропускаем
                    continue
        
        # Считаем трассы, которые скоро обновятся (старше 90 дней)
        old_routes = 0
        for route in active_routes:
            setup_date_str = route.setup_date
            if setup_date_str:
                try:
                    # Парсим дату в формате DD.MM.YYYY
                    setup_date = datetime.strptime(setup_date_str, '%d.%m.%Y').date()
                    if (today - setup_date).days > 90:
                        old_routes += 1
                except ValueError:
                    # Если дата в неправильном формате, пропускаем
                    continue
        
        # Получаем статистику для отображения
        total_routes = all_routes.count()
        active_routes_count = active_routes.count()
        inactive_routes_count = total_routes - active_routes_count
        
        # Получаем уникальных авторов и цвета для фильтров
        authors_list = list(active_routes.values_list('author', flat=True).distinct())
        colors_list = list(active_routes.values_list('color', flat=True).distinct())
        
        context = {
            'routes': active_routes,  # Показываем только активные трассы
            'total_routes': total_routes,
            'active_routes': active_routes_count,
            'inactive_routes': inactive_routes_count,
            'new_routes': new_routes,  # Новые трассы (младше 30 дней)
            'old_routes': old_routes,  # Трассы старше 90 дней
            'data_source': 'SQLite база данных - только активные трассы',
            'authors_list': authors_list,
            'colors_list': colors_list,
        }
        
        logger.info(f"Загружена главная страница с {active_routes_count} активными трассами из {total_routes} общих из SQLite. Новых трасс: {new_routes}, старых трасс: {old_routes}")
        return render(request, 'home.html', context)
        
    except Exception as e:
        logger.error(f"Ошибка при загрузке главной страницы: {str(e)}")
        return render(request, 'home.html', {
            'error': 'Ошибка при загрузке данных из базы данных',
            'routes': [],
            'total_routes': 0,
            'active_routes': 0,
            'inactive_routes': 0,
            'new_routes': 0,
            'old_routes': 0,
            'data_source': 'Ошибка подключения',
            'authors_list': [],
            'colors_list': [],
        })


@api_view(['POST'])
def export_to_google_sheets(request):
    """Экспорт всех трасс в Google Sheets"""
    try:
        # Получаем все трассы
        routes = Route.objects.all()
        routes_data = RouteSerializer(routes, many=True).data
        
        # Синхронизируем с Google Sheets
        sync = RoutesGoogleSheetsSync()
        success = sync.export_routes_to_sheets(routes_data)
        
        if success:
            logger.info(f"Экспортировано {len(routes_data)} трасс в Google Sheets")
            return Response({
                'message': f'Успешно экспортировано {len(routes_data)} трасс в Google Sheets',
                'exported_count': len(routes_data)
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Ошибка при экспорте в Google Sheets'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        logger.error(f"Ошибка при экспорте в Google Sheets: {str(e)}")
        return Response(
            {'error': 'Внутренняя ошибка сервера'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def import_from_google_sheets(request):
    """Импорт трасс из Google Sheets"""
    try:
        sync = RoutesGoogleSheetsSync()
        routes_data = sync.import_routes_from_sheets()
        
        if not routes_data:
            return Response({
                'error': 'Не удалось импортировать данные из Google Sheets'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Создаем трассы из импортированных данных
        created_count = 0
        errors = []
        
        for route_data in routes_data:
            try:
                serializer = RouteSerializer(data=route_data)
                if serializer.is_valid():
                    serializer.save()
                    created_count += 1
                    logger.info(f"Импортирована трасса: {route_data.get('name')}")
                else:
                    errors.append({
                        'route': route_data.get('name', 'Unknown'),
                        'errors': serializer.errors
                    })
            except Exception as e:
                errors.append({
                    'route': route_data.get('name', 'Unknown'),
                    'error': str(e)
                })
        
        logger.info(f"Импортировано {created_count} трасс из Google Sheets")
        return Response({
            'message': f'Импортировано {created_count} трасс из Google Sheets',
            'imported_count': created_count,
            'errors': errors
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Ошибка при импорте из Google Sheets: {str(e)}")
        return Response(
            {'error': 'Внутренняя ошибка сервера'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def google_sheets_status(request):
    """Проверка статуса подключения к Google Sheets"""
    try:
        sync = RoutesGoogleSheetsSync()
        # Пытаемся прочитать заголовки для проверки подключения
        test_data = sync.sheets_manager.read_sheet('A1:Z1')
        
        if test_data:
            return Response({
                'status': 'connected',
                'message': 'Google Sheets подключен успешно'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'disconnected',
                'message': 'Не удалось подключиться к Google Sheets'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"Ошибка проверки статуса Google Sheets: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Ошибка подключения: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def google_sheets_routes(request):
    """Получение всех трасс из Google Sheets"""
    try:
        sync = RoutesGoogleSheetsSync()
        routes_data = sync.import_routes_from_sheets()
        
        if routes_data:
            logger.info(f"Загружено {len(routes_data)} трасс из Google Sheets")
            return Response({
                'routes': routes_data,
                'count': len(routes_data),
                'source': 'google_sheets'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'routes': [],
                'count': 0,
                'source': 'google_sheets',
                'message': 'Нет данных в Google Sheets'
            }, status=status.HTTP_200_OK)
            
    except Exception as e:
        logger.error(f"Ошибка загрузки трасс из Google Sheets: {str(e)}")
        return Response(
            {'error': 'Ошибка загрузки данных из Google Sheets'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def admin_panel_view(request):
    """Админ-панель для управления трассами"""
    try:
        from datetime import datetime, timedelta
        
        # Получаем данные из SQLite базы данных
        all_routes = Route.objects.all()
        active_routes = Route.objects.filter(is_active=True)
        
        # Получаем текущую дату
        today = datetime.now().date()
        
        # Считаем статистику
        total_routes = all_routes.count()
        active_routes_count = active_routes.count()
        inactive_routes_count = total_routes - active_routes_count
        
        # Считаем новые трассы (младше 30 дней)
        new_routes = 0
        for route in active_routes:
            setup_date_str = route.setup_date
            if setup_date_str:
                try:
                    setup_date = datetime.strptime(setup_date_str, '%d.%m.%Y').date()
                    if (today - setup_date).days <= 30:
                        new_routes += 1
                except ValueError:
                    continue
        
        # Считаем трассы, которые скоро обновятся (старше 90 дней)
        old_routes = 0
        for route in active_routes:
            setup_date_str = route.setup_date
            if setup_date_str:
                try:
                    setup_date = datetime.strptime(setup_date_str, '%d.%m.%Y').date()
                    if (today - setup_date).days > 90:
                        old_routes += 1
                except ValueError:
                    continue
        
        context = {
            'routes': all_routes,  # Показываем все трассы в админке
            'total_routes': total_routes,
            'active_routes': active_routes_count,
            'inactive_routes': inactive_routes_count,
            'new_routes': new_routes,
            'old_routes': old_routes,
            'data_source': 'SQLite база данных - все трассы',
        }
        
        logger.info(f"Загружена админ-панель с {total_routes} трассами из SQLite")
        return render(request, 'admin_panel.html', context)
        
    except Exception as e:
        logger.error(f"Ошибка при загрузке админ-панели: {str(e)}")
        return render(request, 'admin_panel.html', {
            'error': 'Ошибка при загрузке данных из SQLite',
            'routes': [],
            'total_routes': 0,
            'active_routes': 0,
            'inactive_routes': 0,
            'new_routes': 0,
            'old_routes': 0,
            'data_source': 'Ошибка загрузки данных'
        })


def export_routes_csv(request):
    """Экспорт всех трасс в CSV формате"""
    try:
        # Получаем все активные трассы
        routes = Route.objects.filter(is_active=True).order_by('route_number')
        
        # Создаем HTTP ответ с CSV
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="traссы_{len(routes)}_шт_{datetime.now().strftime("%Y%m%d")}.csv"'
        
        # Добавляем BOM для корректного отображения кириллицы в Excel
        response.write('\ufeff')
        
        # Создаем CSV writer
        writer = csv.writer(response)
        
        # Записываем заголовки
        writer.writerow(['№ Трассы', 'Дорожка', 'Название', 'Сложность', 'Цвет', 'Автор', 'Дата накрутки', 'Описание'])
        
        # Записываем данные
        for route in routes:
            writer.writerow([
                route.route_number,
                route.track_lane,
                route.name,
                route.difficulty,
                route.color,
                route.author,
                route.setup_date,
                route.description or ''
            ])
        
        logger.info(f"Экспортировано {len(routes)} трасс в CSV")
        return response
        
    except Exception as e:
        logger.error(f"Ошибка при экспорте CSV: {str(e)}")
        return HttpResponse(f"Ошибка при экспорте: {str(e)}", status=500)


def login_view(request):
    """Страница входа в админ панель"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            admin = AdminUser.objects.get(username=username, is_active=True)
            if admin.check_password(password):
                # Успешный вход
                admin.last_login = timezone.now()
                admin.save()
                
                # Сохраняем ID администратора в сессии
                request.session['admin_id'] = admin.id
                request.session['admin_username'] = admin.username
                request.session['admin_name'] = admin.full_name
                
                logger.info(f"Успешный вход администратора: {admin.username}")
                return redirect('admin-panel')
            else:
                error = "Неверный пароль"
        except AdminUser.DoesNotExist:
            error = "Пользователь не найден"
        except Exception as e:
            logger.error(f"Ошибка при входе: {str(e)}")
            error = "Ошибка при входе в систему"
    else:
        error = None
    
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    """Выход из админ панели"""
    if 'admin_id' in request.session:
        logger.info(f"Выход администратора: {request.session.get('admin_username')}")
        del request.session['admin_id']
        del request.session['admin_username']
        del request.session['admin_name']
    
    return redirect('login')


def check_admin_auth(request):
    """Проверка аутентификации администратора"""
    return 'admin_id' in request.session


@api_view(['POST'])
def create_admin_user(request):
    """Создание админ пользователя"""
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        full_name = request.data.get('full_name', 'Администратор')
        
        if not username or not password:
            return Response({
                'success': False,
                'message': 'Логин и пароль обязательны'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Проверяем, существует ли уже такой пользователь
        if AdminUser.objects.filter(username=username).exists():
            return Response({
                'success': False,
                'message': 'Пользователь с таким логином уже существует'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Создаем нового админ пользователя
        admin = AdminUser.objects.create(
            username=username,
            full_name=full_name,
            is_active=True
        )
        admin.set_password(password)
        admin.save()
        
        logger.info(f"Создан новый админ пользователь: {username}")
        
        return Response({
            'success': True,
            'message': f'Админ пользователь {username} создан успешно',
            'admin_id': admin.id
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Ошибка при создании админ пользователя: {e}")
        return Response({
            'success': False,
            'message': f'Ошибка при создании админ пользователя: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def admin_panel_view(request):
    """Админ панель с проверкой аутентификации"""
    # Проверяем аутентификацию
    if not check_admin_auth(request):
        return redirect('login')
    
    # Получаем информацию об администраторе
    admin_id = request.session.get('admin_id')
    try:
        admin = AdminUser.objects.get(id=admin_id)
    except AdminUser.DoesNotExist:
        # Если администратор не найден, очищаем сессию
        request.session.flush()
        return redirect('login')
    
    # Получаем все трассы
    routes = Route.objects.all().order_by('track_lane', 'route_number')
    
    # Получаем уникальные значения для фильтров
    difficulties = sorted(set(Route.objects.values_list('difficulty', flat=True)))
    authors = sorted(set(Route.objects.values_list('author', flat=True)))
    colors = sorted(set(Route.objects.values_list('color', flat=True)))
    
    context = {
        'routes': routes,
        'difficulties': difficulties,
        'authors': authors,
        'colors': colors,
        'admin_name': admin.full_name,
        'admin_username': admin.username,
        'total_routes': routes.count(),
        'active_routes': routes.filter(is_active=True).count(),
        'inactive_routes': routes.filter(is_active=False).count(),
    }
    
    logger.info(f"Загружена админ-панель с {routes.count()} трассами из SQLite")
    return render(request, 'admin_panel.html', context)
