from django.contrib import admin

# Register your models here.
from .models import Product,Customer,User,Seller,Orders,PlatformApiCall
class OrderAdmin(admin.ModelAdmin):
    
    list_display:["__all__"]
admin.site.register(Product)
admin.site.register(Orders,OrderAdmin)
admin.site.register(PlatformApiCall)

