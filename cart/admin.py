from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('created', 'updated')


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_key', 'get_total_items', 'get_total_price', 'created')
    list_filter = ('created',)
    search_fields = ('user__username', 'session_key')
    readonly_fields = ('created', 'updated')
    inlines = [CartItemInline]
    
    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = 'Total Items'
    
    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Total Price'


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'get_total_price', 'created')
    list_filter = ('created',)
    search_fields = ('product__name', 'cart__user__username')
    readonly_fields = ('created', 'updated')
    
    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Total Price'


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
