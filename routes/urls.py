from django.urls import path
from . import views

urlpatterns = [
    # Основные CRUD операции с трассами
    path('routes/', views.RouteListCreateView.as_view(), name='route-list-create'),
    path('routes/<int:pk>/', views.RouteDetailView.as_view(), name='route-detail'),
    
    # Массовые операции
    path('routes/bulk/', views.RouteBulkOperationsView.as_view(), name='route-bulk-operations'),
    path('routes/bulk-update/', views.route_bulk_update, name='route-bulk-update'),
    
    # Дополнительные endpoints
    path('routes/search/', views.route_search, name='route-search'),
    path('routes/authors/', views.route_authors, name='route-authors'),
    path('routes/colors/', views.route_colors, name='route-colors'),
    path('routes/<int:pk>/toggle-active/', views.route_toggle_active, name='route-toggle-active'),
    path('difficulty-levels/', views.difficulty_levels, name='difficulty-levels'),
    path('stats/', views.route_stats, name='route-stats'),
    
    # Google Sheets интеграция
    path('google-sheets/export/', views.export_to_google_sheets, name='export-to-google-sheets'),
    path('google-sheets/import/', views.import_from_google_sheets, name='import-from-google-sheets'),
    path('google-sheets/status/', views.google_sheets_status, name='google-sheets-status'),
    path('google-sheets/routes/', views.google_sheets_routes, name='google-sheets-routes'),
    
    # Аутентификация
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/', views.admin_panel_view, name='admin-panel'),
    path('admin/create/', views.create_admin_user, name='create-admin'),
    
    # Экспорт данных
    path('routes/export-csv/', views.export_routes_csv, name='export-routes-csv'),
]
