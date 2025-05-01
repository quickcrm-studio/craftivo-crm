from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from decimal import Decimal
import random
import uuid

from customers.models import Customer
from products.models import Product, ProductVariation
from orders.models import Order, OrderItem, OrderStatus

class Command(BaseCommand):
    help = 'Creates sample orders for testing and demonstration'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Number of sample orders to create',
        )
        
        parser.add_argument(
            '--customers',
            type=int,
            default=20,
            help='Number of additional sample customers to create',
        )

    def handle(self, *args, **options):
        # Create additional customers if requested
        if options['customers'] > 0:
            self.create_sample_customers(options['customers'])
        
        # Create sample orders
        with transaction.atomic():
            self.create_sample_orders(options['count'])
            
    def create_sample_customers(self, count):
        """Create additional sample customers."""
        created_count = 0
        
        # List of sample first names
        first_names = [
            'Sophia', 'Jackson', 'Olivia', 'Liam', 'Emma', 'Noah', 'Ava', 'Ethan',
            'Isabella', 'Mason', 'Charlotte', 'Lucas', 'Amelia', 'Oliver', 'Mia',
            'Elijah', 'Harper', 'James', 'Evelyn', 'Benjamin', 'Abigail', 'Logan',
            'Emily', 'Alexander', 'Elizabeth', 'Daniel', 'Sofia', 'Matthew', 'Avery',
            'Henry', 'Scarlett', 'Jacob', 'Victoria', 'Ryan', 'Camila', 'Owen',
            'Brooklyn', 'Nathan', 'Madison', 'Samuel', 'Luna', 'Sebastian', 'Grace',
            'Jack', 'Chloe', 'Aiden', 'Penelope', 'Luke', 'Layla', 'William'
        ]
        
        # List of sample last names
        last_names = [
            'Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 
            'Wilson', 'Moore', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 
            'Harris', 'Martin', 'Thompson', 'Garcia', 'Martinez', 'Robinson', 'Clark', 
            'Rodriguez', 'Lewis', 'Lee', 'Walker', 'Hall', 'Allen', 'Young', 'Hernandez', 
            'King', 'Wright', 'Lopez', 'Hill', 'Scott', 'Green', 'Adams', 'Baker', 
            'Gonzalez', 'Nelson', 'Carter', 'Mitchell', 'Perez', 'Roberts', 'Turner', 
            'Phillips', 'Campbell', 'Parker', 'Evans', 'Edwards', 'Collins'
        ]
        
        # Cities and states
        cities_states = [
            ('New York', 'NY', '10001'), ('Los Angeles', 'CA', '90001'), 
            ('Chicago', 'IL', '60601'), ('Houston', 'TX', '77001'), 
            ('Philadelphia', 'PA', '19101'), ('Phoenix', 'AZ', '85001'), 
            ('San Antonio', 'TX', '78201'), ('San Diego', 'CA', '92101'), 
            ('Dallas', 'TX', '75201'), ('San Jose', 'CA', '95101'),
            ('Austin', 'TX', '78701'), ('Indianapolis', 'IN', '46201'), 
            ('Jacksonville', 'FL', '32201'), ('San Francisco', 'CA', '94101'), 
            ('Columbus', 'OH', '43201'), ('Charlotte', 'NC', '28201'), 
            ('Fort Worth', 'TX', '76101'), ('Detroit', 'MI', '48201'), 
            ('El Paso', 'TX', '79901'), ('Memphis', 'TN', '38101'),
            ('Seattle', 'WA', '98101'), ('Denver', 'CO', '80201'), 
            ('Washington', 'DC', '20001'), ('Boston', 'MA', '02101'), 
            ('Nashville', 'TN', '37201'), ('Baltimore', 'MD', '21201'), 
            ('Oklahoma City', 'OK', '73101'), ('Portland', 'OR', '97201'), 
            ('Las Vegas', 'NV', '89101'), ('Milwaukee', 'WI', '53201')
        ]
        
        # Communication preferences
        comm_choices = ['email', 'phone', 'sms']
        
        # Status choices
        status_choices = [Customer.ACTIVE, Customer.NEW, Customer.LEAD, Customer.INACTIVE, Customer.FORMER]
        status_weights = [0.6, 0.15, 0.1, 0.1, 0.05]  # Weights for random selection
        
        for i in range(count):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@example.com"
            
            # Check if this email already exists
            if Customer.objects.filter(email=email).exists():
                continue
                
            # Generate phone number
            phone = f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            
            # Choose random city/state
            city, state, postal_code = random.choice(cities_states)
            
            # Generate address
            street_number = random.randint(100, 9999)
            street_names = ['Main St', 'Oak Ave', 'Maple Rd', 'Washington Blvd', 'Park Ave', 
                           'Cedar Ln', 'Elm St', 'Lake Dr', 'Pine St', 'River Rd']
            street = f"{street_number} {random.choice(street_names)}"
            
            # Create address strings
            address = f"{street}, {city}, {state} {postal_code}"
            
            # Create customer
            customer = Customer.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                shipping_address=address,
                billing_address=address,
                status=random.choices(status_choices, weights=status_weights)[0],
                notes=f"Sample customer {i+1}",
                accepts_marketing=random.choice([True, False]),
                preferred_communication=random.choice(comm_choices),
            )
            created_count += 1
            
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} additional sample customers'))
    
    def create_sample_orders(self, count):
        """Create sample orders with items."""
        # Get all customers and products
        customers = list(Customer.objects.all())
        products = list(Product.objects.filter(status=Product.ACTIVE))
        
        if not customers:
            self.stdout.write(self.style.ERROR('No customers found in the database. Please create customers first.'))
            return
            
        if not products:
            self.stdout.write(self.style.ERROR('No active products found in the database. Please create products first.'))
            return
        
        # Payment methods
        payment_methods = ['Credit Card', 'PayPal', 'Bank Transfer', 'Cash on Delivery']
        
        # Order statuses with weights
        order_statuses = [
            Order.PENDING, Order.PROCESSING, Order.SHIPPED, 
            Order.DELIVERED, Order.CANCELLED, Order.REFUNDED
        ]
        status_weights = [0.15, 0.25, 0.2, 0.3, 0.05, 0.05]
        
        # Payment statuses with weights
        payment_statuses = [
            Order.PAYMENT_PENDING, Order.PAYMENT_PAID, 
            Order.PAYMENT_FAILED, Order.PAYMENT_REFUNDED
        ]
        payment_weights = [0.2, 0.7, 0.05, 0.05]
        
        # Shipping carriers
        carriers = ['UPS', 'FedEx', 'USPS', 'DHL', '']
        
        # Creators for status history
        creators = ['admin', 'staff', 'system', 'john.doe', 'jane.smith']
        
        # Order creation date range (last 6 months)
        end_date = timezone.now()
        start_date = end_date - timedelta(days=180)
        
        created_count = 0
        for i in range(count):
            # Select a random customer
            customer = random.choice(customers)
            
            # Generate a random date in the past 180 days
            days_ago = random.randint(0, 180)
            created_date = end_date - timedelta(days=days_ago)
            
            # Generate order status and payment status based on weighted choices
            order_status = random.choices(order_statuses, weights=status_weights)[0]
            payment_status = random.choices(payment_statuses, weights=payment_weights)[0]
            
            # Make payment status consistent with order status
            if order_status in [Order.SHIPPED, Order.DELIVERED]:
                payment_status = Order.PAYMENT_PAID
            elif order_status == Order.CANCELLED:
                payment_status = random.choice([Order.PAYMENT_PENDING, Order.PAYMENT_FAILED])
            elif order_status == Order.REFUNDED:
                payment_status = Order.PAYMENT_REFUNDED
            
            # Generate shipping and tracking info
            tracking_number = ""
            shipping_carrier = ""
            shipped_at = None
            delivered_at = None
            
            if order_status in [Order.SHIPPED, Order.DELIVERED]:
                tracking_number = f"TRK{random.randint(1000000, 9999999)}"
                shipping_carrier = random.choice(carriers)
                shipped_at = created_date + timedelta(days=random.randint(1, 3))
                
                if order_status == Order.DELIVERED:
                    delivered_at = shipped_at + timedelta(days=random.randint(1, 7))
            
            # Get random number of items for this order (1-5)
            num_items = random.randint(1, 5)
            order_products = random.sample(products, min(num_items, len(products)))
            
            # Calculate subtotal from items
            sub_total = 0
            for product in order_products:
                quantity = random.randint(1, 3)
                sub_total += product.price * quantity
            
            # Calculate other costs
            shipping_amount = Decimal(str(round(random.uniform(5, 15), 2)))
            tax_amount = sub_total * Decimal('0.08')  # 8% tax
            tax_amount = tax_amount.quantize(Decimal('0.01'))
            discount_amount = Decimal('0.00')
            
            # Apply discount to some orders
            if random.random() < 0.3:  # 30% chance of discount
                discount_amount = sub_total * Decimal(str(round(random.uniform(0.05, 0.2), 2)))
                discount_amount = discount_amount.quantize(Decimal('0.01'))
            
            # Calculate total
            total_amount = sub_total + shipping_amount + tax_amount - discount_amount
            
            # Create the order
            order = Order.objects.create(
                order_number=uuid.uuid4().hex[:10].upper(),
                customer=customer,
                status=order_status,
                
                total_amount=total_amount,
                sub_total=sub_total,
                tax_amount=tax_amount,
                shipping_amount=shipping_amount,
                discount_amount=discount_amount,
                
                payment_status=payment_status,
                payment_method=random.choice(payment_methods),
                payment_reference=f"REF{random.randint(100000, 999999)}" if payment_status == Order.PAYMENT_PAID else "",
                
                shipping_name=f"{customer.first_name} {customer.last_name}",
                shipping_address=customer.shipping_address,
                shipping_city=customer.shipping_address.split(',')[1].strip() if ',' in customer.shipping_address else "Unknown",
                shipping_state=customer.shipping_address.split(',')[2].strip().split(' ')[0] if ',' in customer.shipping_address and len(customer.shipping_address.split(',')) > 2 else "Unknown",
                shipping_postal_code=customer.shipping_address.split(',')[2].strip().split(' ')[1] if ',' in customer.shipping_address and len(customer.shipping_address.split(',')) > 2 else "00000",
                shipping_country="USA",
                shipping_phone=customer.phone,
                
                billing_name=f"{customer.first_name} {customer.last_name}",
                billing_address=customer.billing_address,
                billing_city=customer.billing_address.split(',')[1].strip() if ',' in customer.billing_address else "Unknown",
                billing_state=customer.billing_address.split(',')[2].strip().split(' ')[0] if ',' in customer.billing_address and len(customer.billing_address.split(',')) > 2 else "Unknown",
                billing_postal_code=customer.billing_address.split(',')[2].strip().split(' ')[1] if ',' in customer.billing_address and len(customer.billing_address.split(',')) > 2 else "00000",
                billing_country="USA",
                
                customer_notes="Please handle with care" if random.random() < 0.2 else "",
                staff_notes="VIP customer" if random.random() < 0.1 else "",
                
                created_at=created_date,
                updated_at=created_date,
                shipped_at=shipped_at,
                delivered_at=delivered_at,
                
                tracking_number=tracking_number,
                shipping_carrier=shipping_carrier,
            )
            
            # Create order items
            for product in order_products:
                # Check if product has variations
                variations = list(product.variations.all())
                variation = random.choice(variations) if variations else None
                
                # Determine quantity
                quantity = random.randint(1, 3)
                
                # Calculate price - use variation price if available
                price = variation.final_price if variation else product.price
                
                # Prepare variation details
                variation_details = None
                if variation:
                    variation_details = {
                        variation.name: variation.value
                    }
                
                # Create the order item
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_variation=variation,
                    product_name=product.name,
                    sku=variation.full_sku if variation else product.sku,
                    price=price,
                    quantity=quantity,
                    line_total=price * quantity,
                    variation_details=variation_details,
                )
            
            # Create order status history
            # Always add initial "pending" status
            OrderStatus.objects.create(
                order=order,
                status=Order.PENDING,
                notes="Order created",
                created_by="system",
                created_at=created_date,
            )
            
            # Add status updates based on current status
            if order_status != Order.PENDING:
                # Processing status (all orders except pending go through this)
                processing_date = created_date + timedelta(days=random.randint(1, 2))
                OrderStatus.objects.create(
                    order=order,
                    status=Order.PROCESSING,
                    notes="Order processing started",
                    created_by=random.choice(creators),
                    created_at=processing_date,
                )
                
                # Further statuses
                if order_status in [Order.SHIPPED, Order.DELIVERED]:
                    OrderStatus.objects.create(
                        order=order,
                        status=Order.SHIPPED,
                        notes=f"Order shipped via {shipping_carrier or 'carrier'}" + (f" with tracking {tracking_number}" if tracking_number else ""),
                        created_by=random.choice(creators),
                        created_at=shipped_at,
                    )
                    
                    if order_status == Order.DELIVERED:
                        OrderStatus.objects.create(
                            order=order,
                            status=Order.DELIVERED,
                            notes="Order delivered successfully",
                            created_by=random.choice(creators),
                            created_at=delivered_at,
                        )
                elif order_status == Order.CANCELLED:
                    cancel_date = processing_date + timedelta(days=random.randint(1, 3))
                    OrderStatus.objects.create(
                        order=order,
                        status=Order.CANCELLED,
                        notes="Order cancelled " + random.choice([
                            "at customer request", 
                            "due to payment failure", 
                            "due to inventory shortage", 
                            "item no longer available"
                        ]),
                        created_by=random.choice(creators),
                        created_at=cancel_date,
                    )
                elif order_status == Order.REFUNDED:
                    # For refunded orders, add both delivered and then refunded
                    delivered_date = processing_date + timedelta(days=random.randint(3, 7))
                    OrderStatus.objects.create(
                        order=order,
                        status=Order.DELIVERED,
                        notes="Order delivered successfully",
                        created_by=random.choice(creators),
                        created_at=delivered_date,
                    )
                    
                    refund_date = delivered_date + timedelta(days=random.randint(1, 14))
                    OrderStatus.objects.create(
                        order=order,
                        status=Order.REFUNDED,
                        notes="Order refunded " + random.choice([
                            "due to customer dissatisfaction", 
                            "item damaged during shipping", 
                            "wrong item shipped", 
                            "customer requested return"
                        ]),
                        created_by=random.choice(creators),
                        created_at=refund_date,
                    )
            
            created_count += 1
            
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} sample orders')) 