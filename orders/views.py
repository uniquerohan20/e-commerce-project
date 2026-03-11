from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from .models import Order, OrderItem, ShippingAddress
from .forms import OrderForm, ShippingAddressForm
from cart.views import get_or_create_cart
import uuid


@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product')
    
    if not cart_items:
        messages.error(request, 'Your cart is empty!')
        return redirect('cart:cart_detail')
    
    # Check stock availability
    for item in cart_items:
        if item.quantity > item.product.stock:
            messages.error(request, f'{item.product.name} is out of stock or insufficient quantity!')
            return redirect('cart:cart_detail')
    
    # Get user's shipping addresses
    shipping_addresses = ShippingAddress.objects.filter(user=request.user)
    default_address = shipping_addresses.filter(is_default=True).first()
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Create order
                order = Order.objects.create(
                    user=request.user,
                    order_id=str(uuid.uuid4())[:8].upper(),
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                    address=form.cleaned_data['address'],
                    city=form.cleaned_data['city'],
                    state=form.cleaned_data['state'],
                    postal_code=form.cleaned_data['postal_code'],
                    country=form.cleaned_data['country'],
                    payment_method=form.cleaned_data['payment_method'],
                    subtotal=cart.get_total_price(),
                    shipping_cost=0,  # You can calculate shipping based on location
                    tax=0,  # You can calculate tax based on location
                    total=cart.get_total_price(),  # Update this with shipping + tax
                )
                
                # Create order items
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        price=item.product.get_effective_price(),
                        quantity=item.quantity
                    )
                    
                    # Update product stock
                    item.product.stock -= item.quantity
                    item.product.save()
                
                # Clear cart
                cart.items.all().delete()
                
                messages.success(request, 'Order placed successfully!')
                return redirect('orders:order_success', order_id=order.order_id)
    else:
        initial_data = {}
        if default_address:
            initial_data = {
                'first_name': default_address.first_name,
                'last_name': default_address.last_name,
                'phone': default_address.phone,
                'address': default_address.address,
                'city': default_address.city,
                'state': default_address.state,
                'postal_code': default_address.postal_code,
                'country': default_address.country,
            }
        
        # Add user email if not in address
        if not initial_data.get('email'):
            initial_data['email'] = request.user.email
        
        form = OrderForm(initial=initial_data)
    
    context = {
        'form': form,
        'cart': cart,
        'cart_items': cart_items,
        'shipping_addresses': shipping_addresses,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def place_order(request):
    # This is handled in checkout view
    return redirect('orders:checkout')


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    
    if order.status in ['pending', 'confirmed']:
        with transaction.atomic():
            # Restore product stock
            for item in order.items.all():
                item.product.stock += item.quantity
                item.product.save()
            
            # Update order status
            order.status = 'cancelled'
            order.save()
            
            messages.success(request, 'Order cancelled successfully!')
    else:
        messages.error(request, 'Cannot cancel this order at this stage!')
    
    return redirect('orders:order_detail', order_id=order.order_id)
