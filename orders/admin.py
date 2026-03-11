from django.contrib import admin
from .models import Order, OrderItem, ShippingAddress


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ()


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'status', 'payment_method', 'payment_status', 'total', 'created')
    list_filter = ('status', 'payment_method', 'payment_status', 'created')
    search_fields = ('order_id', 'user__username', 'user__email')
    readonly_fields = ('order_id', 'created', 'updated')
    inlines = [OrderItemInline]
    
    actions = ['mark_as_shipped', 'mark_as_delivered', 'cancel_order']
    
    def mark_as_shipped(self, request, queryset):
        for order in queryset:
            if order.status == 'processing':
                order.status = 'shipped'
                order.shipped_date = timezone.now()
                order.save()
    mark_as_shipped.short_description = 'Mark selected orders as shipped'
    
    def mark_as_delivered(self, request, queryset):
        for order in queryset:
            if order.status == 'shipped':
                order.status = 'delivered'
                order.delivered_date = timezone.now()
                order.save()
    mark_as_delivered.short_description = 'Mark selected orders as delivered'
    
    def cancel_order(self, request, queryset):
        for order in queryset:
            if order.status in ['pending', 'confirmed']:
                order.status = 'cancelled'
                order.save()
    cancel_order.short_description = 'Cancel selected orders'


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'price', 'quantity', 'get_total_price')
    search_fields = ('order__order_id', 'product__name')
    
    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Total Price'


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_full_name', 'city', 'state', 'is_default', 'created')
    list_filter = ('is_default', 'state', 'created')
    search_fields = ('user__username', 'first_name', 'last_name', 'city')
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Full Name'


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
