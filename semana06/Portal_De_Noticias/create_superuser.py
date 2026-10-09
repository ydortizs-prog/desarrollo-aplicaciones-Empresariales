import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.contrib.auth.models import User

# Create superuser
User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
print('Superusuario creado exitosamente')