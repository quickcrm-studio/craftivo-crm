from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser and assigns admin group'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='admin', help='Username for admin account')
        parser.add_argument('--email', type=str, default='admin@example.com', help='Email for admin account')
        parser.add_argument('--password', type=str, default='adminpassword', help='Password for admin account')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User {username} already exists'))
            return
        
        # Create superuser
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name='Admin',
            last_name='User'
        )
        
        # Add to Administrators group
        try:
            admin_group = Group.objects.get(name='Administrators')
            user.groups.add(admin_group)
            self.stdout.write(self.style.SUCCESS(f'Added {username} to Administrators group'))
        except Group.DoesNotExist:
            self.stdout.write(self.style.WARNING('Administrators group does not exist. Run create_user_groups first.'))
        
        self.stdout.write(self.style.SUCCESS(f'Admin user {username} created successfully')) 