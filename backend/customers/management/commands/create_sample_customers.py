from django.core.management.base import BaseCommand
from django.utils import timezone
from customers.models import Customer
import random

class Command(BaseCommand):
    help = 'Creates sample customers for testing and demonstration'

    def handle(self, *args, **options):
        # Sample data for customers
        sample_customers = [
            {
                'first_name': 'Emma',
                'last_name': 'Watson',
                'email': 'emma.watson@example.com',
                'phone': '555-123-4567',
                'shipping_address': '123 Main St, New York, NY 10001',
                'billing_address': '123 Main St, New York, NY 10001',
                'status': Customer.ACTIVE,
                'notes': 'Frequent buyer of handmade jewelry',
                'accepts_marketing': True,
                'preferred_communication': 'email',
            },
            {
                'first_name': 'Michael',
                'last_name': 'Johnson',
                'email': 'michael.johnson@example.com',
                'phone': '555-234-5678',
                'shipping_address': '456 Oak Ave, Los Angeles, CA 90001',
                'billing_address': '456 Oak Ave, Los Angeles, CA 90001',
                'status': Customer.ACTIVE,
                'notes': 'Prefers custom made items',
                'accepts_marketing': True,
                'preferred_communication': 'phone',
            },
            {
                'first_name': 'Sophia',
                'last_name': 'Garcia',
                'email': 'sophia.garcia@example.com',
                'phone': '555-345-6789',
                'shipping_address': '789 Pine Rd, Chicago, IL 60007',
                'billing_address': '789 Pine Rd, Chicago, IL 60007',
                'status': Customer.NEW,
                'notes': 'Recently made first purchase',
                'accepts_marketing': False,
                'preferred_communication': 'email',
            },
            {
                'first_name': 'William',
                'last_name': 'Chen',
                'email': 'william.chen@example.com',
                'phone': '555-456-7890',
                'shipping_address': '101 Cedar Blvd, Seattle, WA 98101',
                'billing_address': '101 Cedar Blvd, Seattle, WA 98101',
                'status': Customer.INACTIVE,
                'notes': 'No purchases in the last 6 months',
                'accepts_marketing': True,
                'preferred_communication': 'sms',
            },
            {
                'first_name': 'Olivia',
                'last_name': 'Smith',
                'email': 'olivia.smith@example.com',
                'phone': '555-567-8901',
                'shipping_address': '222 Maple St, Boston, MA 02108',
                'billing_address': '222 Maple St, Boston, MA 02108',
                'status': Customer.LEAD,
                'notes': 'Interested in wooden crafts',
                'accepts_marketing': True,
                'preferred_communication': 'email',
            },
            {
                'first_name': 'James',
                'last_name': 'Wilson',
                'email': 'james.wilson@example.com',
                'phone': '555-678-9012',
                'shipping_address': '333 Elm Dr, Austin, TX 78701',
                'billing_address': '333 Elm Dr, Austin, TX 78701',
                'status': Customer.ACTIVE,
                'notes': 'Wholesale customer for local shop',
                'accepts_marketing': False,
                'preferred_communication': 'phone',
            },
            {
                'first_name': 'Ava',
                'last_name': 'Brown',
                'email': 'ava.brown@example.com',
                'phone': '555-789-0123',
                'shipping_address': '444 Birch Lane, Portland, OR 97201',
                'billing_address': '444 Birch Lane, Portland, OR 97201',
                'status': Customer.FORMER,
                'notes': 'Used to be a regular customer',
                'accepts_marketing': False,
                'preferred_communication': 'email',
            },
            {
                'first_name': 'John',
                'last_name': 'Miller',
                'email': 'john.miller@example.com',
                'phone': '555-890-1234',
                'shipping_address': '555 Walnut Court, Denver, CO 80202',
                'billing_address': '555 Walnut Court, Denver, CO 80202',
                'status': Customer.ACTIVE,
                'notes': 'Buys gifts for special occasions',
                'accepts_marketing': True,
                'preferred_communication': 'email',
            },
            {
                'first_name': 'Isabella',
                'last_name': 'Martinez',
                'email': 'isabella.martinez@example.com',
                'phone': '555-901-2345',
                'shipping_address': '666 Spruce Way, Miami, FL 33101',
                'billing_address': '666 Spruce Way, Miami, FL 33101',
                'status': Customer.NEW,
                'notes': 'Interested in handmade cards',
                'accepts_marketing': True,
                'preferred_communication': 'sms',
            },
            {
                'first_name': 'David',
                'last_name': 'Thompson',
                'email': 'david.thompson@example.com',
                'phone': '555-012-3456',
                'shipping_address': '777 Aspen Circle, Atlanta, GA 30301',
                'billing_address': '777 Aspen Circle, Atlanta, GA 30301',
                'status': Customer.ACTIVE,
                'notes': 'Recurring customer for ceramic items',
                'accepts_marketing': True,
                'preferred_communication': 'email',
            }
        ]

        # Create customers
        created_count = 0
        for customer_data in sample_customers:
            # Check if customer with this email already exists
            if not Customer.objects.filter(email=customer_data['email']).exists():
                Customer.objects.create(**customer_data)
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} sample customers')) 