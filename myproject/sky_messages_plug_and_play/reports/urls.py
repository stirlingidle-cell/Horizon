from django.urls import path
from . import views

# URL routes for the Reports Section
urlpatterns = [
    path('', views.reports_home, name='reports_home'),
    path('team-count/', views.team_count, name='team_count'),
    path('team-count/pdf/', views.team_count_pdf, name='team_count_pdf'),
    path('team-summary/pdf/', views.team_summary_pdf, name='team_summary_pdf'),
    path('without-managers/pdf/', views.teams_without_managers_pdf, name='teams_without_managers_pdf'),
]