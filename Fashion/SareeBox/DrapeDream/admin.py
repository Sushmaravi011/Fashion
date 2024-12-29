from atexit import register
from django.contrib import admin
from .models import *
from .models import Catagory,Product,cart,Favourite
 
 
"""
class CategoryAdmin(admin.ModelAdmin):
  list_display = ('name', 'image', 'description')
admin.site.register(Catagory,CategoryAdmin)
"""
 
admin.site.register(Catagory)
admin.site.register(Product)
admin.site.register(cart)
admin.site.register(Favourite)

