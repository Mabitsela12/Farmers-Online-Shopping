from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Address(models.Model):
    name = models.CharField(max_length=100)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    shipping_required = models.BooleanField(default=False)

#create customer profile
class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified=models.DateTimeField(User, auto_now=True)
    phone=models.CharField(max_length=20, blank=True)
    address1=models.CharField(max_length=200, blank=True)
    address2=models.CharField(max_length=200, blank=True)
    city=models.CharField(max_length=200, blank=True)
    state=models.CharField(max_length=200, blank=True)
    zipcode=models.CharField(max_length=200, blank=True)
    country=models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username
    
#create a user profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):

    if created:
        user_profile=Profile(user=instance)
        user_profile.save()

#Automate the profile thing
post_save.connect(create_profile, sender=User)


#categories of products
class Category(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural= 'categories'

#customers

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username

#All of our products
class Product(models.Model):
    name=models.CharField(max_length=100)
    price=models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category=models.ForeignKey(Category, on_delete=models.CASCADE,default=1, related_name='products')
    description=models.CharField(max_length=250, default='', blank=True, null=True)
    image=models.ImageField(upload_to='uploads/product/')

    #Add Sale
    is_sale=models.BooleanField(default=False)
    sale_price=models.DecimalField(default=0, decimal_places=2, max_digits=6)

    def __str__(self):
        return self.name

#customer orders
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Example field, replace with appropriate product reference
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, default='')
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'Order {self.id}: {self.product} for {self.customer.user.username}'

# Create your models here.
class Locations(models.Model):
    name = models.CharField(max_length=500)
    zipcode = models.CharField(max_length=200,blank=True, null=True)
    city = models.CharField(max_length=200,blank=True, null=True)
    country = models.CharField(max_length=200,blank=True, null=True)
    adress = models.CharField(max_length=200,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    edited_at = models.DateTimeField(auto_now=True)

    lat = models.CharField(max_length=200,blank=True, null=True)
    lng = models.CharField(max_length=200,blank=True, null=True)
    place_id = models.CharField(max_length=200,blank=True, null=True)

    def __str__(self):
        return self.name
    
class driver(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    license_number = models.CharField(max_length=20)
    car_registration = models.CharField(max_length=20)
    car_make = models.CharField(max_length=100)
    # Replace image_url with ImageField
    image = models.ImageField(upload_to='driver_images', blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.surname}"
