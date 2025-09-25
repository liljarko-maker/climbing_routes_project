from rest_framework import serializers
from .models import Route
import csv
from django.http import HttpResponse


class RouteSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Route"""
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)
    
    class Meta:
        model = Route
        fields = [
            'id',
            'route_number',
            'track_lane',
            'name',
            'difficulty',
            'difficulty_display',
            'color',
            'author',
            'setup_date',
            'description',
            'is_active',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate_difficulty(self, value):
        """Валидация уровня сложности"""
        if value not in [choice[0] for choice in Route.DifficultyLevel.choices]:
            raise serializers.ValidationError("Неверный уровень сложности")
        return value

    def validate_name(self, value):
        """Валидация названия трассы"""
        if not value.strip():
            raise serializers.ValidationError("Название трассы не может быть пустым")
        return value.strip()

    def validate_author(self, value):
        """Валидация имени автора"""
        if not value.strip():
            raise serializers.ValidationError("Имя автора не может быть пустым")
        return value.strip()

    def validate_color(self, value):
        """Валидация цвета"""
        if not value.strip():
            raise serializers.ValidationError("Цвет не может быть пустым")
        return value.strip()
    
    def validate_route_number(self, value):
        """Валидация номера трассы"""
        if value < 1 or value > 140:
            raise serializers.ValidationError("Номер трассы должен быть от 1 до 140")
        return value
    
    def validate_track_lane(self, value):
        """Валидация номера дорожки"""
        if value < 1 or value > 35:
            raise serializers.ValidationError("Номер дорожки должен быть от 1 до 35")
        return value
    
    def validate_setup_date(self, value):
        """Валидация даты накрутки"""
        import re
        # Проверяем формат DD.MM.YYYY
        if not re.match(r'^\d{2}\.\d{2}\.\d{4}$', value):
            raise serializers.ValidationError("Дата должна быть в формате DD.MM.YYYY")
        return value
