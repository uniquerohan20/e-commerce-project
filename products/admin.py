from django.contrib import admin
from .models import Category, Product, ProductImage, Review


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discount_price', 'stock', 'available', 'featured', 'created')
    list_filter = ('available', 'featured', 'created', 'category')
    list_editable = ('price', 'discount_price', 'stock', 'available', 'featured')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    
    def get_discount_percentage(self, obj):
        return obj.get_discount_percentage()
    get_discount_percentage.short_description = 'Discount %'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created')
    list_filter = ('rating', 'created')
    search_fields = ('product__name', 'user__username', 'comment')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Review, ReviewAdmin)
