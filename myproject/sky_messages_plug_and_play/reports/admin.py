from django.contrib import admin
from .models import Department, Team

# Registers report related models so that they can be managed through Django Admin
admin.site.register(Department)
admin.site.register(Team)
