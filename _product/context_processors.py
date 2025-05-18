from django.shortcuts import render, get_object_or_404
from .models import Wishlist, Cart, CartItem, Customer, Product

def wishlist_product_count(request):
    """إرجاع عدد المنتجات في المفضلة للمستخدم في السياق"""
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()        
        count = Wishlist.objects.filter(customer=customer).count() if customer else 0
    else:
        count = 0
    return {"wishlist_count": count}


def cartItem_product_count(request):
    """إرجاع عدد المنتجات في السلة للمستخدم في السياق"""
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        cart = Cart.objects.filter(customer=customer, is_active=True).first()
        count = CartItem.objects.filter(cart=cart).count() if cart else 0
    else:
        count = 0
    return {"cart_count": count}

