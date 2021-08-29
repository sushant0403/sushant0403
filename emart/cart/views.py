from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, Cart_item
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def _cart_id(request):
    cart    = request.session.session_key
    if not cart:
        cart    = request.session.create()
    return cart

def add_cart(request, product_id):
    color = request.get["color"]
    size = request.get["size"]

    product     = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart    =   Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    try:
        cart_item   = Cart_item.objects.get(product=product,cart=cart)
        cart_item.quantity  +=  1
    
    except Cart_item.DoesNotExist:
        cart_item = Cart_item.objects.create(
            product     = product,
            cart        = cart,
            quantity    = 1,
        )
    cart_item.save()

    return redirect('cart')

def sub_cart(request, product_id):
    cart        =   Cart.objects.get(cart_id=_cart_id(request))
    product     =   get_object_or_404(Product, id=product_id)
    cart_item  =   Cart_item.objects.get(cart=cart, product=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart(request, product_id):
    cart        =   Cart.objects.get(cart_id=_cart_id(request))
    product     =   get_object_or_404(Product, id=product_id)
    cart_item  =   Cart_item.objects.get(cart=cart, product=product)
    cart_item.delete() 
    return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None):
    try :
        cart        =   Cart.objects.get(cart_id=_cart_id(request))
        cart_items  =   Cart_item.objects.filter(cart=cart, is_active=True)
        cart_item_count = cart_items.count()

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2*total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass # ignore

    context     ={
        "total"                 :  total,
        "tax"                   :  tax,
        "grand_total"           :  grand_total,
        "quantity"              :  quantity,
        "cart_items"            :  cart_items,
        "cart_item_count"       :  cart_item_count
    }
    return render(request,'cart/cart.html' , context)