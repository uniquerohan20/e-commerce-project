from django.contrib import admin
from .models import UserProfile, Wishlist


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'newsletter_subscription')
    list_filter = ('newsletter_subscription',)
    search_fields = ('user__username', 'user__email', 'phone')


class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created')
    list_filter = ('created',)
    search_fields = ('user__username', 'product__name')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Wishlist, WishlistAdmin)
