import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sky_project.settings")

import django
django.setup()

from django.contrib.auth.models import User
from messages_app.models import Message

ceyda, _ = User.objects.get_or_create(username="ceyda", defaults={
    "email": "ceyda@example.com",
    "first_name": "Ceyda",
    "last_name": "Student",
})
ceyda.set_password("password123")
ceyda.save()

manager, _ = User.objects.get_or_create(username="manager", defaults={
    "email": "manager@sky.example.com",
    "first_name": "Sky",
    "last_name": "Manager",
})
manager.set_password("password123")
manager.save()

if not User.objects.filter(username="admin").exists():
    admin = User.objects.create_superuser("admin", "admin@example.com", "admin123")
    admin.save()

if not Message.objects.filter(subject="Welcome to Sky Engineering Messages").exists():
    Message.objects.create(
        sender=manager,
        receiver=ceyda,
        subject="Welcome to Sky Engineering Messages",
        content="This sample message demonstrates the inbox feature for Student 3.",
        is_draft=False,
    )

print("Demo users ready.")
print("Login as ceyda / password123")
print("Admin login: admin / admin123")
