from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


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
    
    # Номер трассы (1-140, всего 35 дорожек по 4 трассы)
    route_number = models.PositiveIntegerField(
        unique=True,
        validators=[MinValueValidator(1), MaxValueValidator(140)],
        verbose_name='№ трассы',
        help_text='Номер трассы (1-140)'
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
        ordering = ['route_number']
        constraints = [
            models.UniqueConstraint(
                fields=['track_lane', 'route_number'],
                name='unique_lane_route'
            )
        ]

    def __str__(self):
        return f"№{self.route_number} - {self.name} ({self.get_difficulty_display()}) - {self.author}"
    
    def clean(self):
        """Валидация модели"""
        from django.core.exceptions import ValidationError
        
        # Проверяем, что на одной дорожке не больше 4 трасс
        if self.track_lane and self.route_number:
            existing_routes = Route.objects.filter(track_lane=self.track_lane).exclude(pk=self.pk)
            if existing_routes.count() >= 4:
                raise ValidationError(f'На дорожке {self.track_lane} уже максимальное количество трасс (4)')
