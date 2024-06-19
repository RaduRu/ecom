from django.shortcuts import render, redirect 
from .models import *
from django.http import JsonResponse
import json 
import datetime
from . utils import cookieCart, cartData, guestOrder
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 




def store(request):

    data = cartData(request)
    cartItems = data['cartItems']
    
    products = Product.objects.all()
    context = {'products':products, 'cartItems': cartItems}
    return render (request, 'store/store.html', context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items' : items, 'order': order, 'cartItems': cartItems}
    return render (request, 'store/cart.html', context)


def checkout(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items' : items, 'order': order, 'cartItems': cartItems}
    return render (request, 'store/checkout.html', context)

def category(request, foo):
    category = Category.objects.get(name = foo)
    products = Product.objects.filter(category = category)
    return render(request, "category.html", {'products': products, 'category': category})


def updateItem(request):
    data = json.loads(request.body)
    productId = data ['productId']
    action = data ['action']

    print ( 'Action: ', action)
    print ( 'productId: ', productId)

    customer = request.user.customer 
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer = customer, complete = False)

    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)

    if action == 'add' :
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()    
    


    return JsonResponse('Item was added', safe = False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer , complete = False)
        
        
    else:
        customer, order = guestOrder(request, data) 
        

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_tot:
        order.complete = True
    order.save()       

    if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
            )        
            
        

    return JsonResponse('Payment completed!!!', safe = False)


def about(request):
    return render (request, 'about.html',  {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in :) "))
            return redirect('store')
        else:
            messages.success(request, ("There was a problem :/ , try again... "))
            return redirect('login')    
    else:
        return render (request, 'login.html',  {})



def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out.. :( "))
    return redirect ('store')


