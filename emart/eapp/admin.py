from django.contrib import admin
from .models import Category ,Account
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display=('category_name','slug','description','Cat_image')
    list_display_links=('category_name','slug',)
    prepopulated_fields={'slug':('category_name',)}
    
admin.site.register(Category,CategoryAdmin)

      


class AccountAdmin(UserAdmin):
    list_display=('email','first_name','last_name', 'username','last_login','date_joined','is_active',)
    list_display_links=('email','first_name','last_name')
    readonly_fields=('last_login','date_joined')
    ordering=('-date_joined',)

    
    #since we are using custom user model so we have to wite following codes
    filter_horizontal=()
    list_filter=('date_joined','is_active')

    fieldsets=() #make password read only
admin.site.register(Account,AccountAdmin)

