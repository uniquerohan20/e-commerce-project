from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Cart, CartItem
from products.models import Product


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def cart_detail(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product')
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'cart/cart_detail.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)
    
    if product.stock < 1:
        messages.error(request, 'This product is out of stock!')
        return redirect('products:product_detail', id=product.id, slug=product.slug)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f'{product.name} quantity updated in cart!')
        else:
            messages.error(request, 'Cannot add more items than available stock!')
    else:
        messages.success(request, f'{product.name} added to cart!')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total': cart.get_total_items(),
            'message': f'{product.name} added to cart!'
        })
    
    return redirect('cart:cart_detail')


def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)
    
    CartItem.objects.filter(cart=cart, product=product).delete()
    messages.success(request, f'{product.name} removed from cart!')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total': cart.get_total_items(),
            'message': f'{product.name} removed from cart!'
        })
    
    return redirect('cart:cart_detail')


def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        cart_item.delete()
        messages.success(request, 'Item removed from cart!')
    elif quantity <= cart_item.product.stock:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cart updated successfully!')
    else:
        messages.error(request, 'Cannot add more items than available stock!')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total': cart_item.cart.get_total_items(),
            'item_total': cart_item.get_total_price(),
            'cart_total_price': cart_item.cart.get_total_price(),
        })
    
    return redirect('cart:cart_detail')


def clear_cart(request):
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    messages.success(request, 'Cart cleared successfully!')
    return redirect('cart:cart_detail')


@require_GET
def cart_count_api(request):
    cart = get_or_create_cart(request)
    return JsonResponse({'count': cart.get_total_items()})
