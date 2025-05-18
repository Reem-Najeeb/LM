from django.shortcuts import render
from _account.models import CustomerBaby
from _product.models import Product
from django.db.models import Subquery, OuterRef, Avg
from django.db.models.functions import Coalesce
from django.db.models import OrderBy
from django.db.models import Avg, FloatField

# Create your views here.
def index(request):
     # 3. آخر 3 منتجات تمت إضافتها
    # latest_products = Product.objects.order_by('-created_at')[:3]


    # top_rated_products = Product.objects.annotate(
    #     avg_rating=Avg('reviews__rating')
    # ).order_by('avg_rating')[:3]

    top_rated_products = Product.objects.annotate(
        avg_rating=Coalesce(Avg('reviews__rating'), 0.0, output_field=FloatField())
    ).order_by('-avg_rating')[:3]

    latest_products = Product.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('-product_created_at')[:3]

    context = {
    'top_rated_products': top_rated_products, 
    'latest_products': latest_products,
    }
    return render(request , 'pages/index.html', context)

def contactUs(request):
    context = {
       
    }
    return render(request , 'pages/contactUs.html', context)

def aboutUs(request):
    babies = CustomerBaby.objects.all()[:4]  #  أول أربعة أطفال
    context = {'babies': babies}
    return render(request , 'pages/aboutUs.html', context)

# # Products
# def products(request):
#     context = {
       
#     }
#     return render(request , 'pages/aboutUs.html', context)

# def product(request , pro_id):
#     context = {
       
#     }
#     return render(request , 'pages/aboutUs.html', context)
