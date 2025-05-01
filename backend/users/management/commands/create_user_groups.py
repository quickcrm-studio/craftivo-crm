from django.core.management.base import BaseCommand
from users.utils import create_groups_with_permissions

class Command(BaseCommand):
    help = 'Creates user groups with appropriate permissions'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating user groups...'))
        create_groups_with_permissions()
        self.stdout.write(self.style.SUCCESS('User groups created successfully!')) 