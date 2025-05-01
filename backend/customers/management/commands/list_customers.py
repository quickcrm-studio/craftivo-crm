from django.core.management.base import BaseCommand
from customers.models import Customer

class Command(BaseCommand):
    help = 'Lists all customers in the database'

    def handle(self, *args, **options):
        customers = Customer.objects.all()
        
        self.stdout.write(self.style.SUCCESS(f'Total customers: {customers.count()}'))
        self.stdout.write('\nCustomer List:')
        self.stdout.write('-' * 80)
        
        for i, customer in enumerate(customers, 1):
            self.stdout.write(
                f"{i}. {customer.get_full_name()} ({customer.email})\n"
                f"   Status: {customer.status}\n"
                f"   Phone: {customer.phone}\n"
                f"   Joined: {customer.date_joined.strftime('%Y-%m-%d')}\n"
                f"   Notes: {customer.notes[:50]}{'...' if len(customer.notes) > 50 else ''}\n"
            )
        
        # Status counts
        status_counts = {}
        for status_choice in Customer.CUSTOMER_STATUS_CHOICES:
            status_code = status_choice[0]
            status_counts[status_code] = Customer.objects.filter(status=status_code).count()
        
        self.stdout.write('\nCustomer Status Summary:')
        self.stdout.write('-' * 80)
        for status_choice in Customer.CUSTOMER_STATUS_CHOICES:
            status_code = status_choice[0]
            status_name = status_choice[1]
            count = status_counts[status_code]
            self.stdout.write(f"{status_name}: {count} customers") 