from django.contrib import admin
from .models import Cart,Cart_item
# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display=('cart_id','date_added')

admin.site.register(Cart,CartAdmin)

class Cart_itemAdmin(admin.ModelAdmin):
    list_display=('cart','product','quantity','is_active')

admin.site.register(Cart_item,Cart_itemAdmin)
