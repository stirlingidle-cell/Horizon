from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('sent/', views.sent, name='sent'),
    path('drafts/', views.drafts, name='drafts'),
    path('new/', views.new_message, name='new_message'),
    path('view/<int:message_id>/', views.view_message, name='view_message'),
    path('delete/<int:message_id>/', views.delete_message, name='delete_message'),
]
