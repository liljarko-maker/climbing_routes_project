from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.hashers import make_password, check_password


class Route(models.Model):
    """Модель трассы на скалодроме"""
    
    class DifficultyLevel(models.TextChoices):
        """Уровни сложности трасс (французская система)"""
        GRADE_4 = '4', '4'
        GRADE_4_5 = '4-5', '4-5'
        GRADE_5 = '5', '5'
        GRADE_5_PLUS = '5+', '5+'
        GRADE_6A = '6a', '6a'
        GRADE_6A_PLUS = '6a+', '6a+'
        GRADE_6B = '6b', '6b'
        GRADE_6B_PLUS = '6b+', '6b+'
        GRADE_6C = '6c', '6c'
        GRADE_6C_PLUS = '6c+', '6c+'
        GRADE_7A = '7a', '7a'
        GRADE_7A_PLUS = '7a+', '7a+'
        GRADE_7B = '7b', '7b'
        GRADE_7B_PLUS = '7b+', '7b+'
        GRADE_7C = '7c', '7c'
        GRADE_7C_PLUS = '7c+', '7c+'
        GRADE_8A = '8a', '8a'
        GRADE_8A_PLUS = '8a+', '8a+'
        GRADE_8B = '8b', '8b'
        GRADE_8B_PLUS = '8b+', '8b+'
        GRADE_8C = '8c', '8c'
        GRADE_9A = '9a', '9a'
        GRADE_UNKNOWN = '-', '-'
    
    # Номер трассы (автоматический, последовательный)
    route_number = models.PositiveIntegerField(
        verbose_name='№ трассы',
        help_text='Номер трассы (автоматический)'
    )
    
    # Номер дорожки (1-35 дорожек, по 4 трассы на дорожке)
    track_lane = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(35)],
        verbose_name='№ дорожки',
        help_text='Номер дорожки (1-35)'
    )
    
    # Название трассы
    name = models.CharField(
        max_length=200, 
        verbose_name='Название',
        help_text='Название трассы'
    )
    
    # Категория сложности
    difficulty = models.CharField(
        max_length=10,
        choices=DifficultyLevel.choices,
        verbose_name='Сложность',
        help_text='Уровень сложности трассы'
    )
    
    # Цвет трассы
    color = models.CharField(
        max_length=50,
        verbose_name='Цвет',
        help_text='Цвет трассы (например: красный, синий, зеленый)'
    )
    
    # Автор трассы
    author = models.CharField(
        max_length=100,
        verbose_name='Автор трассы',
        help_text='Имя автора трассы'
    )
    
    # Дата накрутки
    setup_date = models.CharField(
        max_length=10,
        verbose_name='Дата накрутки',
        help_text='Дата когда трасса была накручена (DD.MM.YYYY)'
    )
    
    # Описание
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
        help_text='Дополнительное описание трассы'
    )
    
    # Статус активности (активна/скручена)
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна',
        help_text='Активна ли трасса (не скручена)'
    )
    
    # Дата создания записи
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания записи',
        help_text='Дата и время создания записи в системе'
    )

    class Meta:
        verbose_name = 'Трасса'
        verbose_name_plural = 'Трассы'
        ordering = ['track_lane', 'route_number']
        constraints = []

    def __str__(self):
        return f"№{self.route_number} - {self.name} ({self.get_difficulty_display()}) - {self.author}"
    
    def save(self, *args, **kwargs):
        """Переопределяем save для автоматического назначения номера трассы"""
        if not self.route_number and self.track_lane:
            # Вычисляем номер трассы на основе дорожки и позиции на дорожке
            # Формула: (track_lane - 1) * 4 + position_on_lane + 1
            existing_routes_on_lane = Route.objects.filter(track_lane=self.track_lane).exclude(pk=self.pk)
            position_on_lane = existing_routes_on_lane.count()  # 0, 1, 2, 3
            self.route_number = (self.track_lane - 1) * 4 + position_on_lane + 1
        # Запускаем полную валидацию модели перед сохранением, чтобы ограничения сработали везде
        self.full_clean()
        super().save(*args, **kwargs)
    
    def clean(self):
        """Валидация модели"""
        from django.core.exceptions import ValidationError
        from datetime import datetime, date
        
        # Проверяем, что на одной дорожке не больше 4 трасс
        if self.track_lane:
            existing_routes = Route.objects.filter(track_lane=self.track_lane).exclude(pk=self.pk)
            if existing_routes.count() >= 4:
                raise ValidationError(f'На дорожке {self.track_lane} уже максимальное количество трасс (4)')

            # Запрет двух трасс одного цвета на одной дорожке (без учета регистра)
            if self.color:
                same_color_qs = Route.objects.filter(
                    track_lane=self.track_lane,
                    color__iexact=self.color
                ).exclude(pk=self.pk)
                if same_color_qs.exists():
                    raise ValidationError(
                        f"На дорожке {self.track_lane} уже есть трасса с цветом '{self.color}'"
                    )

        # Дата накрутки не может быть в будущем (ожидается формат DD.MM.YYYY)
        if self.setup_date:
            try:
                parsed = datetime.strptime(self.setup_date.strip(), "%d.%m.%Y").date()
                if parsed > date.today():
                    raise ValidationError("Дата накрутки не может быть в будущем")
            except ValueError:
                # Формат даты проверяется на уровне сериализатора; здесь дублируем защиту
                raise ValidationError("Дата накрутки должна быть в формате DD.MM.YYYY")
        
        # Проверяем дубликаты на той же и смежных дорожках (±1)
        # Критерии дубликата: совпадают название (без учета регистра и лишних пробелов),
        # сложность и цвет (без учета регистра и пробелов)
        if self.track_lane and self.name and self.difficulty and self.color:
            normalized_name = (self.name or '').strip().lower()
            normalized_color = (self.color or '').strip().lower()
            lanes_to_check = [self.track_lane]
            if self.track_lane > 1:
                lanes_to_check.append(self.track_lane - 1)
            if self.track_lane < 35:
                lanes_to_check.append(self.track_lane + 1)
            duplicates_qs = (
                Route.objects
                .filter(track_lane__in=lanes_to_check)
                .exclude(pk=self.pk)
            )
            for r in duplicates_qs:
                if (r.name or '').strip().lower() == normalized_name \
                   and (r.difficulty or '') == self.difficulty \
                   and (r.color or '').strip().lower() == normalized_color:
                    adjacent_note = 'смежной ' if r.track_lane != self.track_lane else ''
                    raise ValidationError(
                        f"Похожая трасса уже существует на {adjacent_note}дорожке {r.track_lane}: {r.name} ({r.difficulty}, {r.color})"
                    )
        
    
    @classmethod
    def renumber_routes(cls):
        """Перенумеровать все трассы по дорожкам"""
        from django.db import transaction
        
        with transaction.atomic():
            # Получаем все трассы и создаем список для перенумерации
            all_routes = list(cls.objects.all().order_by('track_lane', 'id'))
            
            # Группируем трассы по дорожкам
            routes_by_lane = {}
            for route in all_routes:
                if route.track_lane not in routes_by_lane:
                    routes_by_lane[route.track_lane] = []
                routes_by_lane[route.track_lane].append(route)
            
            # Перенумеровываем трассы
            for lane, routes_on_lane in routes_by_lane.items():
                for position, route in enumerate(routes_on_lane):
                    new_route_number = (lane - 1) * 4 + position + 1
                    # Обновляем напрямую в базе данных, минуя save()
                    cls.objects.filter(pk=route.pk).update(route_number=new_route_number)


class AdminUser(models.Model):
    """Модель администратора для входа в админ панель"""
    
    username = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Логин',
        help_text='Логин администратора'
    )
    
    password_hash = models.CharField(
        max_length=128,
        verbose_name='Хеш пароля',
        help_text='Хешированный пароль'
    )
    
    full_name = models.CharField(
        max_length=100,
        verbose_name='Полное имя',
        help_text='Полное имя администратора'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен',
        help_text='Активен ли администратор'
    )
    
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания',
        help_text='Дата создания аккаунта'
    )
    
    last_login = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Последний вход',
        help_text='Дата и время последнего входа'
    )

    class Meta:
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'
        ordering = ['username']

    def __str__(self):
        return f"{self.full_name} ({self.username})"
    
    def set_password(self, raw_password):
        """Установить пароль (хеширование)"""
        self.password_hash = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Проверить пароль"""
        return check_password(raw_password, self.password_hash)
    
    def save(self, *args, **kwargs):
        # Если пароль не хеширован, хешируем его
        if not self.password_hash.startswith('pbkdf2_'):
            self.password_hash = make_password(self.password_hash)
        super().save(*args, **kwargs)
