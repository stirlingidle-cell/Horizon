from django.contrib import admin
from django.urls import path, include
from messages_app import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('admin/', admin.site.urls),
    path('messages/', include('messages_app.urls')),
    path('reports/', include('reports.urls')),
]
