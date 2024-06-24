import os
import sys
import django
from django.core.management import call_command
from django.db.utils import IntegrityError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medtrace.settings')
django.setup()

def create_groups():
    from django.contrib.auth.models import Group, Permission

    nurse_permissions = [
        'view_product',
        'view_producttotalstock',
        'view_productbatchstock',
        'view_productbatchstage',
        'view_productbatchstagehistory',
    ]
    technician_permissions = [
        'add_product',
        'change_product',
        'delete_product',
        'add_producttotalstock',
        'change_producttotalstock',
        'delete_producttotalstock',
        'add_productbatchstock',
        'change_productbatchstock',
        'delete_productbatchstock',
        'add_productbatchstage',
        'change_productbatchstage',
        'delete_productbatchstage',
    ]

    nurse_group, created = Group.objects.get_or_create(name='Nurse')
    technician_group, created = Group.objects.get_or_create(name='Technician')

    def add_permissions_to_group(group, permissions):
        for perm in permissions:
            try:
                permission = Permission.objects.get(codename=perm)
                if not group.permissions.filter(codename=perm).exists():
                    group.permissions.add(permission)
            except Permission.DoesNotExist:
                print(f"Permission {perm} does not exist")

    add_permissions_to_group(nurse_group, nurse_permissions)
    add_permissions_to_group(technician_group, technician_permissions)

def create_superuser():
    try:
        call_command('createsuperuser', '--noinput', '--username', 'admin', '--email', 'admin@example.com')
    except Exception as e:
        print(e)
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.get(username='admin')
    user.set_password('159753')
    user.save()

def create_users():
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import Group

    User = get_user_model()

    users_info = [
        {'username': 'enfermeiro', 'password': '123456', 'email': 'enfermeiro@example.com', 'group': 'Nurse'},
        {'username': 'tecnico', 'password': '123456', 'email': 'tecnico@example.com', 'group': 'Technician'},
    ]

    for user_info in users_info:
        user, created = User.objects.get_or_create(username=user_info['username'], defaults={'email': user_info['email']})
        if created:
            user.set_password(user_info['password'])
            user.save()
        group = Group.objects.get(name=user_info['group'])
        user.groups.add(group)

def create_products():
    from products.models import Product

    categories = [
        { 'value': 'surgical', 'label': 'Surgical - Instrumentos Cirúrgicos' },
        { 'value': 'imaging', 'label': 'Imaging - Equipamentos de Visualização' },
        { 'value': 'anesthesia', 'label': 'Anesthesia - Dispositivos de Anestesia' },
        { 'value': 'catheterization', 'label': 'Catheterization - Material de Cateterização e Drenagem' },
        { 'value': 'dental', 'label': 'Dental - Instrumental Odontológico' },
        { 'value': 'containers', 'label': 'Containers - Recipientes e Acessórios' },
        { 'value': 'obstetric', 'label': 'Obstetric - Instrumental para Parto' },
        { 'value': 'ppe', 'label': 'PPE - Equipamento de Proteção Individual (Personal Protective Equipment)' },
    ]

    units = [
        { 'value': 'pc', 'label': 'Peça' },
        { 'value': 'set', 'label': 'Conjunto' },
        { 'value': 'unit', 'label': 'Unidade' },
        { 'value': 'pk', 'label': 'Pacote' },
        { 'value': 'box', 'label': 'Caixa' },
    ]

    products = [
        { 'name': 'Bisturi', 'sku': 'SKU001', 'category': 'surgical', 'unit': 'pc' },
        { 'name': 'Estetoscópio', 'sku': 'SKU002', 'category': 'imaging', 'unit': 'unit' },
        { 'name': 'Máquina de Anestesia', 'sku': 'SKU003', 'category': 'anesthesia', 'unit': 'unit' },
        { 'name': 'Cateter Venoso', 'sku': 'SKU004', 'category': 'catheterization', 'unit': 'pk' },
        { 'name': 'Pinça Odontológica', 'sku': 'SKU005', 'category': 'dental', 'unit': 'pc' },
        { 'name': 'Recipiente de Amostra', 'sku': 'SKU006', 'category': 'containers', 'unit': 'box' },
        { 'name': 'Pinça Obstétrica', 'sku': 'SKU007', 'category': 'obstetric', 'unit': 'pc' },
        { 'name': 'Máscara Cirúrgica', 'sku': 'SKU008', 'category': 'ppe', 'unit': 'box' },
        { 'name': 'Seringa', 'sku': 'SKU009', 'category': 'surgical', 'unit': 'pk' },
    ]

    for product in products:
        try:
            Product.objects.create(
                name=product['name'],
                sku=product['sku'],
                category=product['category'],
                unit=product['unit']
            )
        except IntegrityError:
            print(f"Product with SKU {product['sku']} already exists")

if __name__ == "__main__":
    create_groups()
    create_superuser()
    create_users()
    create_products()
