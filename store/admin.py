from django.contrib import admin
from .models import Category, Customer, Product, Order, Profile, Locations
from django.contrib.auth.models import User
from .models import *


admin.site.register(Locations)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)
admin.site.register(driver)

#Mix profile and user info
#class ProfileInline(admin.StackedInline)