import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Category, Product

class Command(BaseCommand):
    help = 'Creates sample handmade product categories and products'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample handmade product categories and products...')
        
        # Create Categories
        categories = [
            {
                'name': 'Handmade Jewelry',
                'description': 'Unique and beautiful handmade jewelry pieces including necklaces, bracelets, earrings, and rings.'
            },
            {
                'name': 'Pottery & Ceramics',
                'description': 'Handcrafted pottery and ceramic items including mugs, bowls, plates, and decorative pieces.'
            },
            {
                'name': 'Textile & Fiber Arts',
                'description': 'Handmade textile items including quilts, woven goods, embroidery, and fiber art decorations.'
            },
            {
                'name': 'Woodworking',
                'description': 'Handcrafted wooden items including furniture, cutting boards, decorative pieces, and utensils.'
            },
            {
                'name': 'Candles & Soaps',
                'description': 'Handmade candles and soaps in various scents, shapes, and sizes.'
            },
            {
                'name': 'Paper Goods',
                'description': 'Handmade paper products including cards, stationery, journals, and paper art.'
            },
        ]
        
        # Create subcategories
        subcategories = [
            {
                'parent': 'Handmade Jewelry',
                'name': 'Necklaces',
                'description': 'Handcrafted necklaces made with various materials and techniques.'
            },
            {
                'parent': 'Handmade Jewelry',
                'name': 'Earrings',
                'description': 'Handcrafted earrings including studs, hoops, dangles, and more.'
            },
            {
                'parent': 'Handmade Jewelry',
                'name': 'Bracelets',
                'description': 'Handcrafted bracelets including cuffs, bangles, beaded, and more.'
            },
            {
                'parent': 'Pottery & Ceramics',
                'name': 'Mugs & Cups',
                'description': 'Handcrafted ceramic mugs and cups in various designs and sizes.'
            },
            {
                'parent': 'Pottery & Ceramics',
                'name': 'Bowls & Plates',
                'description': 'Handcrafted ceramic bowls and plates for serving and decoration.'
            },
            {
                'parent': 'Woodworking',
                'name': 'Cutting Boards',
                'description': 'Handmade wooden cutting boards in various woods and designs.'
            },
            {
                'parent': 'Woodworking',
                'name': 'Home Decor',
                'description': 'Handcrafted wooden home decor items and wall art.'
            },
            {
                'parent': 'Candles & Soaps',
                'name': 'Scented Candles',
                'description': 'Handmade scented candles in various fragrances and containers.'
            },
            {
                'parent': 'Candles & Soaps',
                'name': 'Artisan Soaps',
                'description': 'Handcrafted artisan soaps in various scents and ingredients.'
            },
            {
                'parent': 'Textile & Fiber Arts',
                'name': 'Knitted Items',
                'description': 'Handmade knitted items including scarves, hats, blankets, and more.'
            },
            {
                'parent': 'Textile & Fiber Arts',
                'name': 'Embroidery',
                'description': 'Handmade embroidery art and embroidered items.'
            },
            {
                'parent': 'Paper Goods',
                'name': 'Greeting Cards',
                'description': 'Handmade greeting cards for various occasions.'
            },
            {
                'parent': 'Paper Goods',
                'name': 'Journals & Notebooks',
                'description': 'Handmade journals and notebooks with unique covers and bindings.'
            },
        ]
        
        # Create main categories
        category_objects = {}
        for category_data in categories:
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                defaults={
                    'description': category_data['description'],
                    'slug': slugify(category_data['name'])
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
            else:
                self.stdout.write(f'Category already exists: {category.name}')
            
            category_objects[category.name] = category
        
        # Create subcategories
        subcategory_objects = {}
        for subcat_data in subcategories:
            parent_category = category_objects.get(subcat_data['parent'])
            if parent_category:
                subcategory, created = Category.objects.get_or_create(
                    name=subcat_data['name'],
                    defaults={
                        'description': subcat_data['description'],
                        'slug': slugify(subcat_data['name']),
                        'parent': parent_category
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created subcategory: {subcategory.name} (parent: {parent_category.name})'))
                else:
                    self.stdout.write(f'Subcategory already exists: {subcategory.name}')
                
                subcategory_objects[subcategory.name] = subcategory
        
        # Sample products
        products = [
            # Jewelry - Necklaces
            {
                'name': 'Handcrafted Beaded Necklace',
                'category': 'Necklaces',
                'price': 42.99,
                'cost': 15.50,
                'description': 'Beautiful handcrafted beaded necklace made with semi-precious stones and sterling silver clasp. Each piece is unique with careful attention to detail.',
                'sku': 'JLY-NCK-001',
                'stock_quantity': 12,
                'weight': 45,
            },
            {
                'name': 'Wire-Wrapped Pendant Necklace',
                'category': 'Necklaces',
                'price': 38.50,
                'cost': 14.25,
                'description': 'Stunning wire-wrapped pendant necklace featuring a natural crystal. The intricate wire work showcases the beauty of the stone, creating a one-of-a-kind piece.',
                'sku': 'JLY-NCK-002',
                'stock_quantity': 8,
                'weight': 35,
            },
            
            # Jewelry - Earrings
            {
                'name': 'Copper Leaf Earrings',
                'category': 'Earrings',
                'price': 28.99,
                'cost': 9.75,
                'description': 'Delicate copper earrings hand-forged into beautiful leaf shapes. These lightweight earrings feature surgical steel ear wires for sensitive ears.',
                'sku': 'JLY-EAR-001',
                'stock_quantity': 15,
                'weight': 12,
            },
            {
                'name': 'Ceramic Stud Earrings Set',
                'category': 'Earrings',
                'price': 32.50,
                'cost': 10.80,
                'description': 'Set of three pairs of ceramic stud earrings, each hand-painted with unique designs. Perfect for mixing and matching with any outfit.',
                'sku': 'JLY-EAR-002',
                'stock_quantity': 20,
                'weight': 15,
            },
            
            # Jewelry - Bracelets
            {
                'name': 'Woven Friendship Bracelet',
                'category': 'Bracelets',
                'price': 18.99,
                'cost': 5.25,
                'description': 'Handwoven friendship bracelet made with colorful embroidery thread. Each bracelet features a unique pattern that won\'t fade or wear away.',
                'sku': 'JLY-BRC-001',
                'stock_quantity': 25,
                'weight': 8,
            },
            {
                'name': 'Adjustable Leather Cuff',
                'category': 'Bracelets',
                'price': 34.99,
                'cost': 12.50,
                'description': 'Hand-tooled leather cuff bracelet with adjustable snap closure. Features a beautiful mandala design that is carefully pressed into the leather.',
                'sku': 'JLY-BRC-002',
                'stock_quantity': 18,
                'weight': 30,
            },
            
            # Pottery - Mugs
            {
                'name': 'Ceramic Speckled Mug',
                'category': 'Mugs & Cups',
                'price': 26.99,
                'cost': 9.00,
                'description': 'Handcrafted ceramic mug with a beautiful speckled glaze. Perfect for your morning coffee or tea. Each mug is wheel-thrown and unique.',
                'sku': 'POT-MUG-001',
                'stock_quantity': 30,
                'weight': 350,
            },
            {
                'name': 'Ceramic Travel Mug with Lid',
                'category': 'Mugs & Cups',
                'price': 38.50,
                'cost': 14.75,
                'description': 'Handmade ceramic travel mug with silicone lid. Keeps your drinks hot while on the go. Features a comfortable handle and non-slip base.',
                'sku': 'POT-MUG-002',
                'stock_quantity': 15,
                'weight': 425,
            },
            
            # Pottery - Bowls
            {
                'name': 'Ceramic Serving Bowl Set',
                'category': 'Bowls & Plates',
                'price': 78.99,
                'cost': 32.50,
                'description': 'Set of three nested ceramic serving bowls. Perfect for salads, pasta, or serving snacks. Each bowl is hand-thrown and glazed with food-safe materials.',
                'sku': 'POT-BWL-001',
                'stock_quantity': 12,
                'weight': 1200,
            },
            {
                'name': 'Ceramic Ramen Bowl',
                'category': 'Bowls & Plates',
                'price': 32.99,
                'cost': 12.25,
                'description': 'Large handcrafted ceramic ramen bowl. Perfect for soup, noodles, or rice dishes. Features a beautiful glazed interior with a matte exterior.',
                'sku': 'POT-BWL-002',
                'stock_quantity': 18,
                'weight': 550,
            },
            
            # Woodworking - Cutting Boards
            {
                'name': 'Walnut End Grain Cutting Board',
                'category': 'Cutting Boards',
                'price': 89.99,
                'cost': 35.25,
                'description': 'Handcrafted end grain cutting board made from solid walnut. The end grain construction helps preserve your knife edges and provides a durable cutting surface.',
                'sku': 'WOD-CTB-001',
                'stock_quantity': 8,
                'weight': 1800,
                'length': 45,
                'width': 30,
                'height': 4,
            },
            {
                'name': 'Maple and Cherry Serving Board',
                'category': 'Cutting Boards',
                'price': 65.99,
                'cost': 24.50,
                'description': 'Beautiful handcrafted serving board made from maple and cherry woods. Features an integrated handle and juice groove. Perfect for charcuterie or serving appetizers.',
                'sku': 'WOD-CTB-002',
                'stock_quantity': 15,
                'weight': 1200,
                'length': 50,
                'width': 25,
                'height': 2.5,
            },
            
            # Woodworking - Home Decor
            {
                'name': 'Wooden Wall Clock',
                'category': 'Home Decor',
                'price': 78.50,
                'cost': 30.25,
                'description': 'Handcrafted wooden wall clock made from reclaimed oak. Features hand-cut numbers and a quiet sweep movement. Each clock is unique due to the natural variations in the wood.',
                'sku': 'WOD-DEC-001',
                'stock_quantity': 10,
                'weight': 850,
                'length': 30,
                'width': 30,
                'height': 3,
            },
            {
                'name': 'Wooden Desk Organizer',
                'category': 'Home Decor',
                'price': 45.99,
                'cost': 18.75,
                'description': 'Handcrafted wooden desk organizer with compartments for pens, pencils, and other office supplies. Made from solid cherry wood with a natural oil finish.',
                'sku': 'WOD-DEC-002',
                'stock_quantity': 20,
                'weight': 750,
                'length': 25,
                'width': 15,
                'height': 10,
            },
            
            # Candles
            {
                'name': 'Lavender Soy Candle',
                'category': 'Scented Candles',
                'price': 24.99,
                'cost': 9.50,
                'description': 'Handmade soy wax candle with essential lavender oil. Burns cleanly for approximately 40 hours. Comes in a reusable glass container.',
                'sku': 'CND-SCT-001',
                'stock_quantity': 35,
                'weight': 300,
            },
            {
                'name': 'Vanilla & Cinnamon Candle Set',
                'category': 'Scented Candles',
                'price': 38.50,
                'cost': 14.25,
                'description': 'Set of two handmade candles with vanilla and cinnamon scents. Perfect for creating a warm, inviting atmosphere. Made with all-natural soy wax and cotton wicks.',
                'sku': 'CND-SCT-002',
                'stock_quantity': 25,
                'weight': 500,
            },
            
            # Soaps
            {
                'name': 'Goat Milk Soap Collection',
                'category': 'Artisan Soaps',
                'price': 32.99,
                'cost': 12.50,
                'description': 'Collection of four handmade goat milk soaps in different scents: lavender, rose, eucalyptus, and unscented. Gentle on skin and naturally moisturizing.',
                'sku': 'SOP-ART-001',
                'stock_quantity': 30,
                'weight': 400,
            },
            {
                'name': 'Exfoliating Coffee Soap',
                'category': 'Artisan Soaps',
                'price': 12.99,
                'cost': 4.25,
                'description': 'Handmade exfoliating soap made with real coffee grounds. Helps scrub away dead skin while the caffeine helps reduce inflammation. Made with all-natural ingredients.',
                'sku': 'SOP-ART-002',
                'stock_quantity': 40,
                'weight': 120,
            },
            
            # Textiles - Knitted Items
            {
                'name': 'Hand-Knitted Infinity Scarf',
                'category': 'Knitted Items',
                'price': 48.99,
                'cost': 18.75,
                'description': 'Soft, chunky infinity scarf hand-knitted with premium merino wool. Warm and cozy for cold weather. Available in multiple colors.',
                'sku': 'TXT-KNT-001',
                'stock_quantity': 15,
                'weight': 250,
            },
            {
                'name': 'Knitted Baby Blanket',
                'category': 'Knitted Items',
                'price': 65.99,
                'cost': 25.50,
                'description': 'Hand-knitted baby blanket made with super soft cotton yarn. Perfect for newborns and infants. Machine washable and durable.',
                'sku': 'TXT-KNT-002',
                'stock_quantity': 10,
                'weight': 400,
                'length': 90,
                'width': 70,
            },
            
            # Textiles - Embroidery
            {
                'name': 'Floral Embroidery Hoop Art',
                'category': 'Embroidery',
                'price': 35.99,
                'cost': 13.25,
                'description': 'Hand-embroidered floral design in a wooden hoop. Ready to hang on your wall. Each piece is unique and made with high-quality embroidery floss.',
                'sku': 'TXT-EMB-001',
                'stock_quantity': 12,
                'weight': 150,
            },
            {
                'name': 'Embroidered Tea Towel Set',
                'category': 'Embroidery',
                'price': 28.50,
                'cost': 10.75,
                'description': 'Set of two hand-embroidered cotton tea towels with botanical designs. Practical and beautiful addition to any kitchen. Machine washable.',
                'sku': 'TXT-EMB-002',
                'stock_quantity': 20,
                'weight': 180,
            },
            
            # Paper Goods - Greeting Cards
            {
                'name': 'Handmade Birthday Card Set',
                'category': 'Greeting Cards',
                'price': 18.99,
                'cost': 6.50,
                'description': 'Set of five handmade birthday cards with envelopes. Each card features a unique design with hand-stamped and embellished details.',
                'sku': 'PPR-CRD-001',
                'stock_quantity': 25,
                'weight': 100,
            },
            {
                'name': 'Watercolor Thank You Cards',
                'category': 'Greeting Cards',
                'price': 16.50,
                'cost': 5.75,
                'description': 'Pack of eight handmade thank you cards with hand-painted watercolor designs. Comes with matching envelopes and blank insides for your personal message.',
                'sku': 'PPR-CRD-002',
                'stock_quantity': 30,
                'weight': 120,
            },
            
            # Paper Goods - Journals
            {
                'name': 'Leather-Bound Journal',
                'category': 'Journals & Notebooks',
                'price': 42.99,
                'cost': 16.25,
                'description': 'Handcrafted leather-bound journal with handmade paper. Features a wrap-around tie closure and 120 unlined pages perfect for sketching or writing.',
                'sku': 'PPR-JNL-001',
                'stock_quantity': 15,
                'weight': 350,
            },
            {
                'name': 'Marbled Paper Notebook',
                'category': 'Journals & Notebooks',
                'price': 22.99,
                'cost': 8.50,
                'description': 'Handmade notebook with a cover featuring original hand-marbled paper. Contains 80 pages of high-quality lined paper perfect for journaling or note-taking.',
                'sku': 'PPR-JNL-002',
                'stock_quantity': 25,
                'weight': 200,
            },
        ]
        
        # Create products
        for product_data in products:
            # Find the right category
            category = subcategory_objects.get(product_data['category'])
            if not category:
                self.stdout.write(self.style.WARNING(f"Couldn't find category {product_data['category']} for product {product_data['name']}"))
                continue
            
            # Set a random status with a bias toward active
            status_choices = [Product.ACTIVE, Product.ACTIVE, Product.ACTIVE, Product.DRAFT, Product.ARCHIVED]
            status = random.choice(status_choices)
            
            # Set random reorder threshold
            reorder_threshold = random.choice([3, 5, 8, 10])
            
            # Create product if it doesn't exist
            product, created = Product.objects.get_or_create(
                sku=product_data['sku'],
                defaults={
                    'name': product_data['name'],
                    'slug': slugify(product_data['name']),
                    'description': product_data['description'],
                    'category': category,
                    'price': Decimal(str(product_data['price'])),
                    'cost': Decimal(str(product_data['cost'])),
                    'stock_quantity': product_data['stock_quantity'],
                    'reorder_threshold': reorder_threshold,
                    'status': status,
                    'weight': product_data.get('weight'),
                    'length': product_data.get('length'),
                    'width': product_data.get('width'),
                    'height': product_data.get('height'),
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.name} (category: {category.name})'))
            else:
                self.stdout.write(f'Product already exists: {product.name}')
        
        # Final summary
        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {Category.objects.count()} categories and {Product.objects.count()} products!'
        )) 