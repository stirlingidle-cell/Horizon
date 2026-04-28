from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'receiver', 'is_draft', 'is_read', 'timestamp')
    list_filter = ('is_draft', 'is_read', 'timestamp')
    search_fields = ('subject', 'content', 'sender__username', 'receiver__username')
