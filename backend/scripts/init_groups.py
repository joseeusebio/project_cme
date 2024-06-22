import os
import sys
import django
from django.db import migrations

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medtrace.settings')
django.setup()

def create_groups():
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType

    nurse_permissions = [
        'view_tracability',
        'view_reports',
    ]
    technician_permissions = [
        'perform_process',
    ]
    client_permissions = [
        'request_materials',
    ]

    nurse_group, created = Group.objects.get_or_create(name='Nurse')
    technician_group, created = Group.objects.get_or_create(name='Technician')
    client_group, created = Group.objects.get_or_create(name='Client')

    content_type = ContentType.objects.get_for_model(Permission)

    for perm in nurse_permissions:
        permission, created = Permission.objects.get_or_create(
            codename=perm,
            name=f'Can {perm}',
            content_type=content_type
        )
        nurse_group.permissions.add(permission)

    for perm in technician_permissions:
        permission, created = Permission.objects.get_or_create(
            codename=perm,
            name=f'Can {perm}',
            content_type=content_type
        )
        technician_group.permissions.add(permission)

    for perm in client_permissions:
        permission, created = Permission.objects.get_or_create(
            codename=perm,
            name=f'Can {perm}',
            content_type=content_type
        )
        client_group.permissions.add(permission)

if __name__ == "__main__":
    create_groups()
