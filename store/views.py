from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm
from django import forms
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Locations, driver
import random 
from .models import Order
from django.shortcuts import render, get_object_or_404

@login_required
def trace_order(request, order_id):
    # Retrieve the order for the logged-in user based on the order ID
    order = get_object_or_404(Order, id=order_id, customer=request.user.customer)

    return render(request, 'order_details.html', {'order': order})


def order_list(request):
    # Retrieve all orders from the database
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})


@login_required
def payment_view(request):
    # Ensure the user is authenticated
    if request.method == 'POST':
        # Access the authenticated user's email
        user_email = request.user.email
        # Process the payment using the retrieved email
        # Your payment processing logic here
        return render(request, 'payment_success.html')
    else:
        return render(request, 'payment_form.html')


def payment_success(request):
    return render(request, 'payment_success.html')

def update_password(request):
    if request.user.is_authenticated:
        current_user=request.user
        #Did they fill out the form?
        if request.method == 'POST':
            form=ChangePasswordForm(current_user, request.POST)
            #is the form valid
            if form.is_valid():
                form.save()
                messages.success(request, "Your Password Has Been Updated")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
        else:
            form=ChangePasswordForm(current_user)
        return render(request, 'update_password.html', {'form':form})
        
    else:
        messages.success(request, "You must be logged in to view that page")
        return redirect('home')    



    

def update_user(request):
    if request.user.is_authenticated:
        current_user=User.objects.get(id=request.user.id)
        user_form= UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User Has Been Updated Successfully")
            return redirect('home')
        
        return render(request, 'update_user.html', {'user_form':user_form})
    else:
         messages.success(request, "You Must Be Logged In To Access That Page")
         return redirect('home')


   

def category_summary(request):
    categories=Category.objects.all()
    return render(request, 'category_summary.html',{"categories":categories} )

def category(request, foo):
    #Relace hyphens with spaces
    foo= foo.replace('-', ' ')
    #take the category from the url
    try:
        #look up the category
        category= Category.objects.get(name=foo)
        products=Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})

    except:
        messages.success(request, ("That Category doesn't exist "))
        return redirect('home')
    


def product(request,pk):
    product= Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def home(request):
    products=Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
   if request.method=="POST":
       username= request.POST['username']
       password= request.POST['password']
       user=authenticate(request, username=username, password=password)
       if user is not None:
           login(request, user)
           messages.success(request, ("You have logged in successfully"))
           return redirect('home')
       else:
           messages.error(request, ("Invalid username or password. Please try again.") )
           return render(request, 'login.html', {})

   else:
        return render(request, 'login.html', {}) 
        


def logout_user(request):
    logout(request)
    messages.success(request,("You have been logged out..") )
    return redirect('home')


def register_user(request):
    form= SignUpForm()
    if request.method=="POST":
        form= SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            username= form.cleaned_data['username']
            password= form.cleaned_data['password1']

            #log in user
            user=authenticate(username = username, password = password)
            login(request,user)
            messages.success(request, ("You have registered succesfully"))
            return redirect('home')
        
        else:
            messages.error(request, ("There was an error, please try again"))
            return render(request,'register.html', {'form': form})

    else:
        return render(request, 'register.html', {'form':form})



class MapView(View): 
    template_name = "map.html"

    def get(self, request): 
        key = 'AIzaSyDxuAJBqVhovKJSvB19c8wDJRAipJtGLZc'
        eligible_locations = Locations.objects.filter(place_id__isnull=False)
        locations = []

        for location in eligible_locations:
            data = {
                'lat': float(location.lat),
                'lng': float(location.lng),
                'name': location.name
            }
            locations.append(data)

        # Select one random driver
        drivers = list(driver.objects.all())
        selected_driver = None
        if drivers:
            selected_driver = random.choice(drivers)

        context = {
            "key": key,
            "locations": locations,
            "selected_driver": selected_driver,
        }
        return render(request, self.template_name, context)

