from .models import User,UserManager,Icon,Category,Tag,Product,Order,OrderDetails
from django.contrib.auth import get_user_model
from django.contrib import admin

User = get_user_model()
# Main Section Title
admin.site.site_header = 'From Farm To Home'
# ------------------------------------------
# Order Admin Section
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','email','total_price','payment_type','order_date')
    search_fields = ['user','email']
    list_filter = ('payment_type',)
    ordering = ['id','order_date']
# OrderDetails Admin Section
@admin.register(OrderDetails)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ('product','count','price')
    search_fields = ['product']
    ordering = ['id',]
# Product Admin Section
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','weight','unit','price','category')
    search_fields = ['title','category']
    ordering = ['id',]
# Tag Admin Section
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ['title',]
    ordering = ['id',]
# Category Admin Section
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ['title',]
    ordering = ['id',]
# Icon Admin Section
@admin.register(Icon)
class IconAdmin(admin.ModelAdmin):
    list_display = ('title','url')
    search_fields = ['title',]
    ordering = ['id',]
# User Admin Section
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email','first_name','last_name','superuser','staff','active','create_date')
    search_fields = ['email','first_name','last_name']
    list_filter = ('superuser','staff','active')
    ordering = ['id', 'create_date']
admin.site.register = (User,UserAdmin)
admin.site.register = (UserManager)