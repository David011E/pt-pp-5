from django.contrib import admin
from .models import Product, Category

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'stripe_price_id',
        'price',
        'image',
    )

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'type',
    )

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)