from django.db import migrations

def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')

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
        permission, created = Permission.objects.get_or_create(codename=perm, name=f'Can {perm}', content_type=content_type)
        nurse_group.permissions.add(permission)

    for perm in technician_permissions:
        permission, created = Permission.objects.get_or_create(codename=perm, name=f'Can {perm}', content_type=content_type)
        technician_group.permissions.add(permission)

    for perm in client_permissions:
        permission, created = Permission.objects.get_or_create(codename=perm, name=f'Can {perm}', content_type=content_type)
        client_group.permissions.add(permission)

class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
