from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.contrib import messages
from django.http import JsonResponse
from .models import Order

def order_status(request):
    #id_ord = Order.
    # Logic to retrieve order status data from the database
    # You can pass order status data to the template if needed
    orders = Order
    stus = "Panding"

    context = {'order_id': orders,
               'status_id': stus
               }
    orde=  context
    return render(request, 'order_status.html', orde)

#from .models import Order

def cart_summary(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    
    # Create an order based on the contents of the cart
    if request.method == 'POST':
        # Assuming you have a function to create an order
        order = Order.objects.create(request.user, cart_products, quantities, totals)
        # Optionally, you can clear the cart after creating the order
        cart.clear()
        # Redirect to a page showing order details, or render a template with order details
    
    return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals})


def cart_add(request):
    #get the cart
    cart=Cart(request)
    #test for post
    if request.POST.get('action')=='post':
        #get stuff
        product_id= int(request.POST.get('product_id'))
        product_qty= int(request.POST.get('product_qty'))
        #look up product in DB
        product= get_object_or_404(Product, id=product_id)

        #save to session
        cart.add(product=product, quantity=product_qty)

        # Get Cart Quantity
        cart_quantity=cart.__len__()

        #Return response
        #response=JsonResponse({'Product Name:': product.name})
        response=JsonResponse({'qty:': cart_quantity})
        messages.success(request, ("Product Added To Cart") )
        return response

def cart_delete(request):
    cart=Cart(request)
    if request.POST.get('action')=='post':
        #get stuff
        product_id= int(request.POST.get('product_id'))
        #call delete function in cart
        cart.delete(product=product_id)

        response=JsonResponse({'product':product_id})
        messages.success(request, ("Product Deleted From Shopping Cart") )

        return response

def cart_update(request):
    cart=Cart(request)
    if request.POST.get('action')=='post':
        #get stuff
        product_id= int(request.POST.get('product_id'))
        product_qty= int(request.POST.get('product_qty'))

        cart.update(product= product_id, quantity=product_qty)

        response=JsonResponse({'qty':product_qty})
        messages.success(request, ("Your Cart Has Been Updated") )
        return response
        #return redirect('cart_summary')
    
    