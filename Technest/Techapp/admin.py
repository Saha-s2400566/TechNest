from django.contrib import admin
from .models import Product, CustomUser, Cart
from django.contrib.auth.admin import UserAdmin


# Register Product model with customization
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock', 'is_active')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'desc', 'category')
    ordering = ('-created_at',)
    list_editable = ('price', 'stock', 'is_active')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'desc', 'price')
        }),
        ('Product Details', {
            'fields': ('image', 'category', 'stock')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

# CustomUser admin configuration
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_active')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'phone_number')
        }),
    )

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__username', 'product__name')
    ordering = ('-created_at',)
