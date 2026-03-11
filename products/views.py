from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Product, Category


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    # Featured products
    featured_products = Product.objects.filter(available=True, featured=True)[:4]
    
    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'featured_products': featured_products,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    
    # Get related products
    related_products = Product.objects.filter(category=product.category, available=True).exclude(id=product.id)[:4]
    
    # Get product reviews
    reviews = product.reviews.all().order_by('-created')
    
    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
    }
    return render(request, 'products/product_detail.html', context)


def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(available=True)
    
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
    
    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'products/search.html', context)
