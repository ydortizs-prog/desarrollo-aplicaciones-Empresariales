"""Create editors group (add/change movies, no delete) and test user."""
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType

from movies.models import Movie

ct = ContentType.objects.get_for_model(Movie)
perms = Permission.objects.filter(
    content_type=ct, codename__in=['add_movie', 'change_movie', 'view_movie']
)
group, _ = Group.objects.get_or_create(name='editores')
group.permissions.set(perms)

user, created = User.objects.get_or_create(username='editor1')
user.set_password('editor123')
user.is_staff = True
user.save()
user.groups.add(group)

print('Group perms:', sorted(p.name for p in group.permissions.all()))
print('Can add:', user.has_perm('movies.add_movie'))
print('Can change:', user.has_perm('movies.change_movie'))
print('Can delete:', user.has_perm('movies.delete_movie'))
