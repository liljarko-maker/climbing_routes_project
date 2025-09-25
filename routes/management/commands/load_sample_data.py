from django.core.management.base import BaseCommand
from routes.models import Route


class Command(BaseCommand):
    help = 'Загружает примеры трасс для тестирования'

    def handle(self, *args, **options):
        from datetime import date, timedelta
        
        sample_routes = [
            {
                'route_number': 1,
                'track_number': 1,
                'name': 'Красная линия',
                'difficulty': '4-5',
                'author': 'Иван Петров',
                'color': 'красный',
                'setup_date': date.today() - timedelta(days=30),
                'description': 'Простая трасса для начинающих'
            },
            {
                'route_number': 2,
                'track_number': 1,
                'name': 'Синий маршрут',
                'difficulty': '6A',
                'author': 'Анна Смирнова',
                'color': 'синий',
                'setup_date': date.today() - timedelta(days=25),
                'description': 'Легкая трасса с техничными движениями'
            },
            {
                'route_number': 3,
                'track_number': 1,
                'name': 'Зеленая стена',
                'difficulty': '6B+',
                'author': 'Михаил Козлов',
                'color': 'зеленый',
                'setup_date': date.today() - timedelta(days=20),
                'description': 'Средняя трасса с мощными движениями'
            },
            {
                'route_number': 4,
                'track_number': 2,
                'name': 'Черная дыра',
                'difficulty': '7A+',
                'author': 'Елена Волкова',
                'color': 'черный',
                'setup_date': date.today() - timedelta(days=15),
                'takedown_date': date.today() - timedelta(days=5),
                'description': 'Сложная трасса для опытных скалолазов'
            },
            {
                'route_number': 5,
                'track_number': 2,
                'name': 'Желтый луч',
                'difficulty': '6A+',
                'author': 'Дмитрий Новиков',
                'color': 'желтый',
                'setup_date': date.today() - timedelta(days=10),
                'description': 'Легкая трасса с хорошими зацепами'
            },
            {
                'route_number': 6,
                'track_number': 2,
                'name': 'Фиолетовая мечта',
                'difficulty': '6C',
                'author': 'Ольга Морозова',
                'color': 'фиолетовый',
                'setup_date': date.today() - timedelta(days=8),
                'description': 'Средняя трасса с интересными переходами'
            },
            {
                'route_number': 7,
                'track_number': 3,
                'name': 'Оранжевый взрыв',
                'difficulty': '7B',
                'author': 'Алексей Соколов',
                'color': 'оранжевый',
                'setup_date': date.today() - timedelta(days=5),
                'description': 'Очень сложная трасса с динамичными движениями'
            },
            {
                'route_number': 8,
                'track_number': 3,
                'name': 'Белая стена',
                'difficulty': '8A',
                'author': 'Мария Иванова',
                'color': 'белый',
                'setup_date': date.today() - timedelta(days=3),
                'description': 'Профессиональная трасса с микро-зацепами'
            },
            {
                'route_number': 9,
                'track_number': 3,
                'name': 'Золотая мечта',
                'difficulty': '9A',
                'author': 'Сергей Легенда',
                'color': 'золотой',
                'setup_date': date.today() - timedelta(days=1),
                'description': 'Легендарная трасса мирового класса'
            }
        ]

        created_count = 0
        for route_data in sample_routes:
            route, created = Route.objects.get_or_create(
                name=route_data['name'],
                defaults=route_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Создана трасса: {route.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Трасса уже существует: {route.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Создано {created_count} новых трасс')
        )
