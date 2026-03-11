from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Category, Product, Review
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create sample data for the e-commerce site'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
            {'name': 'Clothing', 'description': 'Fashion and apparel'},
            {'name': 'Books', 'description': 'Books and literature'},
            {'name': 'Home & Garden', 'description': 'Home improvement and garden supplies'},
            {'name': 'Sports', 'description': 'Sports equipment and accessories'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'description': cat_data['description']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))

        # Create sample products
        products_data = [
            {
                'category': 'Electronics',
                'name': 'Smartphone X',
                'description': 'Latest smartphone with advanced features',
                'price': 29999,
                'discount_price': 24999,
                'stock': 50,
                'featured': True,
            },
            {
                'category': 'Electronics',
                'name': 'Laptop Pro',
                'description': 'High-performance laptop for professionals',
                'price': 89999,
                'discount_price': None,
                'stock': 25,
                'featured': True,
            },
            {
                'category': 'Clothing',
                'name': 'Cotton T-Shirt',
                'description': 'Comfortable cotton t-shirt for everyday wear',
                'price': 599,
                'discount_price': 399,
                'stock': 100,
                'featured': False,
            },
            {
                'category': 'Clothing',
                'name': 'Denim Jeans',
                'description': 'Classic denim jeans with perfect fit',
                'price': 1999,
                'discount_price': 1499,
                'stock': 75,
                'featured': False,
            },
            {
                'category': 'Books',
                'name': 'Python Programming',
                'description': 'Complete guide to Python programming',
                'price': 899,
                'discount_price': None,
                'stock': 30,
                'featured': False,
            },
            {
                'category': 'Books',
                'name': 'Web Development',
                'description': 'Modern web development techniques',
                'price': 1299,
                'discount_price': 999,
                'stock': 40,
                'featured': True,
            },
            {
                'category': 'Home & Garden',
                'name': 'Indoor Plant Set',
                'description': 'Set of 5 indoor plants for home decoration',
                'price': 2499,
                'discount_price': 1999,
                'stock': 20,
                'featured': False,
            },
            {
                'category': 'Sports',
                'name': 'Yoga Mat',
                'description': 'Professional yoga mat with extra cushioning',
                'price': 1299,
                'discount_price': None,
                'stock': 60,
                'featured': False,
            },
        ]

        for prod_data in products_data:
            category = Category.objects.get(name=prod_data['category'])
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'slug': slugify(prod_data['name']),
                    'category': category,
                    'description': prod_data['description'],
                    'price': prod_data['price'],
                    'discount_price': prod_data['discount_price'],
                    'stock': prod_data['stock'],
                    'featured': prod_data['featured'],
                    'available': True,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))

        # Create sample reviews
        if not Review.objects.exists():
            products = Product.objects.all()[:3]
            for i, product in enumerate(products):
                user, created = User.objects.get_or_create(
                    username=f'user{i+1}',
                    defaults={
                        'email': f'user{i+1}@example.com',
                        'first_name': f'User{i+1}',
                        'last_name': 'Test'
                    }
                )
                
                Review.objects.create(
                    product=product,
                    user=user,
                    rating=4 + (i % 2),
                    comment=f'Great product! I really love this {product.name}. Highly recommended!'
                )
                self.stdout.write(self.style.SUCCESS(f'Created review for: {product.name}'))

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
