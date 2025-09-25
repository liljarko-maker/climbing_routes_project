from django.contrib import admin
from .models import Route


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    """Админ-панель для управления трассами"""
    list_display = [
        'route_number',
        'track_lane',
        'name', 
        'difficulty', 
        'author', 
        'color',
        'setup_date',
        'is_active',
        'created_at'
    ]
    list_filter = [
        'difficulty', 
        'track_lane',
        'is_active',
        'setup_date',
        'created_at', 
        'author'
    ]
    search_fields = [
        'route_number',
        'name', 
        'author', 
        'color', 
        'description'
    ]
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'route_number']
    ordering = ['route_number']
    
    fieldsets = (
        ('Нумерация', {
            'fields': ('route_number', 'track_lane'),
            'description': 'Номер трассы назначается автоматически'
        }),
        ('Основная информация', {
            'fields': ('name', 'difficulty', 'author', 'color')
        }),
        ('Даты и статус', {
            'fields': ('setup_date', 'is_active')
        }),
        ('Дополнительная информация', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
        ('Системная информация', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
