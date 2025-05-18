from django.shortcuts import render, get_object_or_404
from .models import *
from django.core.paginator import Paginator

from django.core import serializers
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.db.models import OuterRef, Subquery, Avg, Q
from django.db.models import Avg, F
from django.db.models.functions import Coalesce
from django.db.models import OrderBy
from django.db.models import Avg, FloatField


from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal, InvalidOperation


import logging
logger = logging.getLogger(__name__)

# 🔴 Products Page:-

# 0:a:to product page:All 🌸done
def Products_List(request):
    avg_rating_subquery = Review.objects.filter(
        product=OuterRef('pk')
    ).values('product').annotate(avg_rating=Avg('rating')).values('avg_rating')

    # دمج المتوسط في المنتجات
    # product = Product.objects.annotate(avg_rating=Subquery(avg_rating_subquery)).order_by('-id')
    product = Product.objects.annotate(avg_rating=Subquery(avg_rating_subquery)).order_by('?')

    # Pagination
    paginator = Paginator(product, 8)  # تقسيم المنتجات بحيث يظهر 2 في كل صفحة
    page_number = request.GET.get('page')
    products_obj = paginator.get_page(page_number)

    colors = Product.choices_colors
    age_ranges = Product.choices_age_range
    categories = Category.objects.all()


    wishlist_products = []
    cart_items = []
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            wishlist_products = Wishlist.objects.filter(customer=customer).values_list('product_id', flat=True)
            cart = Cart.objects.filter(customer=customer, is_active=True).first()
            if cart:
                cart_items = CartItem.objects.filter(cart=cart).values_list('product_id', flat=True)  # استرجاع معرفات المنتجات في السلة
    
    context = {
        'products': products_obj,  # المنتجات
        'colors': colors,
        'age_ranges': age_ranges,
        'categories': categories,
        'wishlist_products': wishlist_products,
        'cart_items': cart_items,  # المنتجات الموجودة في السلة
    }
    return render(request, "product/_allProducts.html", context)

# 0:b:Load More Products:(Json)🌸done
def Load_More(request):
    offset = int(request.POST.get('offset', 0)) 
    limit = 3

    #  متوسط التقييم لكل منتج
    avg_rating_subquery = Review.objects.filter(
        product=OuterRef('pk')
    ).values('product').annotate(avg_rating=Avg('rating')).values('avg_rating')

    #  المنتجات مع المتوسط  
    products = Product.objects.annotate(avg_rating=Subquery(avg_rating_subquery))[offset:offset + limit]

    totalData = Product.objects.count()

    # التحقق مما إذا كان المستخدم مسجلاً الدخول
    wishlist_products = []
    cart_items = []
    
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            wishlist_products = list(Wishlist.objects.filter(customer=customer).values_list('product_id', flat=True))
            cart = Cart.objects.filter(customer=customer, is_active=True).first()
            if cart:
                cart_items = list(CartItem.objects.filter(cart=cart).values_list('product_id', flat=True))

    products_list = []
    for product in products:
        products_list.append({
            "product_id": product.id,
            "product_name": product.product_name,
            "product_image": getattr(product.product_image, 'url', ''),  # حالة عدم وجود صورة
            "product_selling_price": product.product_selling_price,
            "product_age_range": product.product_age_range,
            "product_gender": product.product_gender,
            "product_color": product.product_color,
            "product_category": product.product_subcategory.category.name, 
            "avg_rating": product.avg_rating or 0,  # وضع 0 إذا مافي تقييمات
            "in_wishlist": product.id in wishlist_products,  # تحقق إذا كان المنتج في المفضلة 
            "in_cart": product.id in cart_items  # تحقق إذا كان المنتج في السلة
        })

    return JsonResponse(data={
        'Products': products_list,
        'totalResult': totalData
    })


# 1:A📢Call function
def get_filtered_products(request, filter_kwargs=None):
    if filter_kwargs is None:
        filter_kwargs = {}

    avg_rating_subquery = Review.objects.filter(
        product=OuterRef('pk')
    ).values('product').annotate(avg_rating=Avg('rating')).values('avg_rating')

    products_qs = Product.objects.filter(**filter_kwargs).annotate(
        avg_rating=Subquery(avg_rating_subquery)
    )

    paginator = Paginator(products_qs, 20)
    page_number = request.GET.get('page')
    products_obj = paginator.get_page(page_number)

    return products_obj
# 1:B📢Call function
def get_common_context(request):
    colors = Product.choices_colors
    age_ranges = Product.choices_age_range
    categories = Category.objects.all()

    wishlist_products = []
    cart_items = []

    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            wishlist_products = Wishlist.objects.filter(customer=customer).values_list('product_id', flat=True)
            cart = Cart.objects.filter(customer=customer, is_active=True).first()
            if cart:
                cart_items = CartItem.objects.filter(cart=cart).values_list('product_id', flat=True)

    return {
        'colors': colors,
        'age_ranges': age_ranges,
        'categories': categories,
        'wishlist_products': wishlist_products,
        'cart_items': cart_items,
    }


# 2:to products page:Filter 🌸done
def Products_from_Link_age(request, age):
    products = get_filtered_products(request, {'product_age_range': age})
    context = get_common_context(request)
    context['products'] = products
    return render(request, "product/_allProducts.html", context)
# 2:to products page:Filter 🌸done
def Products_from_Link_gender(request, gender):
    products = get_filtered_products(request, {'product_gender': gender})
    context = get_common_context(request)
    context['products'] = products
    return render(request, "product/_allProducts.html", context)
# 2:to products page:Filter 🌸done
def Products_from_Link_category(request, category_name):
    category = Category.objects.filter(name__iexact=category_name).first()
    if category:
        products = get_filtered_products(request, {'product_subcategory__category': category})
    else:
        products = Product.objects.none()

    context = get_common_context(request)
    context['products'] = products
    return render(request, "product/_allProducts.html", context)

# 2:to products page:Filter 🌸done
def bestRateProducts(request):
    products = get_filtered_products(request)
    context = get_common_context(request)
    # top_rated_products = Product.objects.annotate(
    #     avg_rating=Coalesce(Avg('reviews__rating'), 0)
    #     ).order_by('-avg_rating')
    
    top_rated_products = Product.objects.annotate(
        avg_rating=Coalesce(Avg('reviews__rating'), 0.0, output_field=FloatField())
    ).order_by('-avg_rating')

    context['products'] = top_rated_products
    return render(request, 'product/_allProducts.html', context)



# 2:to products page:Filter 🌸done
def newArrivalProducts(request):
    products = get_filtered_products(request)
    context = get_common_context(request)
    top_rated_products = Product.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('-product_created_at')

    context['products'] = top_rated_products
    return render(request, 'product/_allProducts.html', context)


# 3:to products page:Search 🌸done
def searchProducts(request):
    products = Product.objects.all()
    name = request.GET.get('searchname', '')
    existing = False

    if name:
        products = products.filter(
            Q(product_name__icontains=name) |
            Q(product_description__icontains=name)
        )
    else:
        existing = False
    colors = Product.choices_colors
    age_ranges = Product.choices_age_range
    categories = Category.objects.all()

    context = {
        'products': products,
        'search_query': name,
        'colors': colors,
        'age_ranges': age_ranges,
        'categories': categories,
        'existing': existing
    }
    return render(request, 'product/_allProducts.html', context)



# 4: count WishList 🌸done
@login_required(login_url='signIn')
def wishlist_count(request):
    """إرجاع عدد المنتجات في المفضلة كـ JSON"""
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        count = Wishlist.objects.filter(customer=customer).count() if customer else 0
    else:
        count = 0
    return JsonResponse({'count': count})

# 4: count Cart 🌸done
@login_required(login_url='signIn')
def cartItem_count(request):
    """إرجاع عدد العناصر في السلة كـ JSON"""
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        cart = Cart.objects.filter(customer=customer, is_active=True).first()
        count = CartItem.objects.filter(cart=cart).count() if cart else 0
    else:
        count = 0
    return JsonResponse({'count': count})

# 5:A add or remove from WishList 🌸done
@login_required(login_url='signIn')
def Add_or_remove_Wishlist(request):
    if not request.user.is_authenticated:
        return JsonResponse({
                'bool': 'error',  
                'message': ' يجب تسجيل الدخول!',
                }, status=401)
        

    pid = request.GET.get('product')
    if not pid:
        return JsonResponse({'error': 'No product ID provided'}, status=400)

    try:
        product = Product.objects.get(pk=pid)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    user = request.user

    try:
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer profile not found'}, status=404)

    wishlist_item = Wishlist.objects.filter(product=product, customer=customer)

    if wishlist_item.exists():
        wishlist_item.delete()
        return JsonResponse({'bool': False})
    else:
        Wishlist.objects.create(product=product, customer=customer)
        return JsonResponse({'bool': True})

# 5:B add or remove from Cart 🌸done
@login_required(login_url='signIn')
def Add_or_Remove_Single_CartItem(request):
    if not request.user.is_authenticated:
        return JsonResponse({
                'bool': 'error',  
                'message': ' يجب تسجيل الدخول!',
                }, status=401)
    product_id = request.GET.get('product_id')
    qty = 1  # الافتراضي 
    user = request.user

    if not product_id:
        return JsonResponse({'error': 'لا يوجد id منتج'}, status=400)

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'لا يوجد منتج'}, status=404)

    # البحث عن العميل
    customer, created = Customer.objects.get_or_create(user=user)

    # التحقق مما إذا كانت السلة غير نشطة، وإنشاء سلة جديدة في هذه الحالة
    cart = Cart.objects.filter(customer=customer, is_active=True).first()
    if not cart:
        cart = Cart.objects.create(customer=customer, is_active=True)

    # البحث عن العنصر في السلة، وإذا كان موجودًا، يتم حذفه
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
    if cart_item:
        cart_item.delete()
        return JsonResponse({'bool': False, 'message': 'تم الحذف'})
    else:
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': qty})
        return JsonResponse({'bool': True, 'message': 'تم الاضافة'})



# 🔴 Single Product Page:-
# 6:A Single Product 🌸done
def Product_Detail(request, pk):
    # 1.product
    single_product= get_object_or_404(Product , pk=pk)
    has_review = False
    # print(has_review)
    try:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            # return JsonResponse({"error": "❌ المستخدم غير موجود!"}, status=400)
            if Review.objects.filter(customer=customer, product=single_product).exists():
                has_review = True
                # print(has_review)
    except Exception as e:
        logger.error(f"يجب تسجيل الدخول : {e}")
    # حساب متوسط تقييم المنتج الرئيسي
    average_rating = Review.objects.filter(product=single_product).aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

    # 1.product.images
    product_images = ProductImage.objects.filter(product=single_product)[:4] 

    # 1.product.wishList:-
    wishlist_products = []
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            wishlist_products = Wishlist.objects.filter(customer=customer).values_list('product_id', flat=True)
            
    # 1.product.rate استعلام لحساب متوسط التقييم للمنتج
    avg_rating_subquery = Review.objects.filter(
        product=OuterRef('pk')
    ).values('product').annotate(avg_rating=Avg('rating')).values('avg_rating')

    # 1.product.reviews
    product_reviews = Review.objects.filter(product=single_product).order_by('-created_at')[:6] 

    # 3.filter استعلام لجلب 3 منتجات فقط بناءً على أي من المعايير المحددة 
    filtered_products = Product.objects.annotate(
        avg_rating=Subquery(avg_rating_subquery)
    ).filter(
    (
        Q(product_age_range=single_product.product_age_range) &
        Q(product_subcategory=single_product.product_subcategory)
    ) &
    ~Q(pk=single_product.pk)
    ).order_by('?')[:3]

    filtered_products_replace = Product.objects.annotate(
        avg_rating=Subquery(avg_rating_subquery)
    ).filter(
         (
            Q(product_age_range=single_product.product_age_range) |
            Q(product_gender=single_product.product_gender) |
            Q(product_subcategory=single_product.product_subcategory)
         )&
    ~Q(pk=single_product.pk)
     ).order_by('?')[:3]  
    

    
    likes_count = Wishlist.objects.filter(product=single_product).count()  # حساب عدد الإعجابات
    print(likes_count)

    print(has_review)

    context = {
        'product' : single_product,
        'products': filtered_products,
        'products_r': filtered_products_replace,
        'product_images': product_images,
        "in_wishlist": Product.id in wishlist_products, 
        'average_rating': average_rating,
        'avg_rating_subquery': avg_rating_subquery,
        'product_reviews': product_reviews,
        # 'likes_count': likes_count,
        'wishlist_products': wishlist_products,
        'has_review': has_review,
    }
    return render(request , 'product/_singleProduct.html', context)

# 6:B 🌸done
@csrf_exempt
@login_required(login_url='signIn')
def Add_or_remove_Wishlist_PD(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({
                'bool': 'error',
                'message': ' يجب تسجيل الدخول!',
                }, status=401)
    print('Her aorw***')
    pid = request.GET.get('product')
    user = request.user

    if not pid:
        return JsonResponse({'error': 'No product ID provided'}, status=400)

    try:
        product = Product.objects.get(pk=pid)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    try:
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=400)

    wishlist_item = Wishlist.objects.filter(product=product, customer=customer)

    if wishlist_item.exists():
        wishlist_item.delete()
        status = False
    else:
        Wishlist.objects.create(product=product, customer=customer)
        status = True

    likes_count = Wishlist.objects.filter(product=product).count()
    return JsonResponse({'bool': status, 'likes_count': likes_count})

# 6:C 🌸done
@csrf_exempt  # تعطيل CSRF مؤقتًا أثناء التصحيح فقط
def add_to_cart_product(request, product_id):
    try:
        print(f"🔍 استقبال طلب إضافة المنتج: {product_id}")

        if request.method != 'POST':
            return JsonResponse({'error': "Invalid request method"}, status=400)

        if not request.user.is_authenticated:
            return JsonResponse({'error': "User not authenticated"}, status=403)

        customer = Customer.objects.filter(user=request.user).first()
        if not customer:
            return JsonResponse({"error": "المستخدم غير موجود!"}, status=400)

        product_qty = request.POST.get('product_qty')
        if not product_qty or not product_qty.isdigit():
            return JsonResponse({'error': "كمية المنتج غير صحيحة!"}, status=400)

        product_qty = int(product_qty)
        # البحث عن المنتج
        try:
            product_check = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': "المنتج غير موجود!"}, status=404)

        # إضافة المنتج إلى السلة
        cart, created = Cart.objects.get_or_create(customer=customer, is_active=True)
        # cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product_check)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product_check, defaults={'quantity': product_qty})

        if not created:
            cart_item.quantity += product_qty
            cart_item.save()
        return JsonResponse({
                'bool': 'success',  # يمكن أن يكون 'success', 'warning', 'error', 'info'
                'message': ' تمت إضافة المنتج إلى السلة بنجاح!',
                }, status=200)
        
        return JsonResponse({'status': "تمت إضافة المنتج إلى السلة بنجاح!"})

    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")
        return JsonResponse({'error': "حدث خطأ في السيرفر!"}, status=500)

# 6:D 🌸done
@login_required
def add_review_product(request, product_id):
    if request.method != 'POST':
        return JsonResponse({'error': "❌ طريقة الطلب غير صحيحة!"}, status=400)

    try:
        customer = Customer.objects.filter(user=request.user).first()
        if not customer:
            return JsonResponse({"error": "❌ المستخدم غير موجود!"}, status=400)

        product = Product.objects.filter(id=product_id).first()
        if not product:
            return JsonResponse({'error': "❌ المنتج غير موجود!"}, status=404)

        if Review.objects.filter(customer=customer, product=product).exists():
            return JsonResponse({
            'bool': 'warning',  # يمكن أن يكون 'success', 'warning', 'error', 'info'
            'message': 'لقد قمت بتقييم هذا المنتج مسبقًا، لا يمكنك إضافة تقييم آخر!',
            }, status=200)
            # return JsonResponse({'warning': "⚠️ لقد قمت بتقييم هذا المنتج مسبقًا، لا يمكنك إضافة تقييم آخر!"}, status=200)

        rating_value = request.POST.get('ratingValue', '').strip()
        rating_text = request.POST.get('ratingtext', '').strip()

        if not rating_value.isnumeric():
            return JsonResponse({'error': "⚠️ يجب إدخال قيمة التقييم كعدد صحيح بين 0 و 5!"}, status=400)

        rating_value = int(rating_value)
        if not (0 <= rating_value <= 5):
            return JsonResponse({
                'bool': 'error',  # يمكن أيضاً استخدام 'warning' للتحذيرات
                'message': 'يجب إدخال قيمة التقييم كعدد صحيح بين 0 و 5!'
            }, status=400)

        if not rating_text:
            return JsonResponse({
                'bool': 'error',
                'message': 'يجب إدخال تعليق التقييم!'
            }, status=200)

        Review.objects.create(
            customer=customer, 
            product=product,   
            rating=rating_value,
            comment=rating_text
        )

        # return JsonResponse({'success': "✅"})
        return JsonResponse({
                'bool': 'success',
                'message': ' تمت إضافة التقييم بنجاح!',
                }, status=200)

    except Exception as e:
        logger.error(f"❌ خطأ غير متوقع: {e}")
        return JsonResponse({'error': "❌ حدث خطأ غير متوقع، يرجى المحاولة لاحقًا."}, status=500)


# 🔴 WishList Page:-
# 7:A 🌸done
@login_required(login_url='signIn')
def wishlist(request):
    wishlist_products = []
    cart_items = []
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        products = Product.objects.filter(wishlist__customer=customer)
        
        if customer:
            wishlist_products = Wishlist.objects.filter(customer=customer).values_list('product_id', flat=True)
            cart = Cart.objects.filter(customer=customer, is_active=True).first()
            if cart:
                # عشان اتاكد موجود في السلة ولا لا للتبديل لكل الايقونات
                cart_items = CartItem.objects.filter(cart=cart).values_list('product_id', flat=True) 
    
    
    # 3 random product 
    # random_products = Product.objects.order_by('?')[:3]
    random_products = Product.objects.annotate(
            avg_rating=Avg('reviews__rating')
        ).order_by('?')[:3]
    context={
        'products_wishlist': products,
        'cart_items': cart_items, 
        'wishlist_products': wishlist_products,
        # 
        'products': random_products,
    }
    return render(request,  "product/wishList.html", context)

# 7:B 🌸done
@login_required(login_url='signIn')
def remove_Wishlist(request):
    product_id = request.GET.get('product_id')
    user = request.user

    if not product_id:
        return JsonResponse({'error': 'لا يوجد id منتج'}, status=400)

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'لا يوجد منتج'}, status=404)

    # البحث عن العميل
    customer, created = Customer.objects.get_or_create(user=user)
    wishlist_item = Wishlist.objects.filter(product=product, customer=customer)

    if wishlist_item.exists():
        wishlist_item.delete()
        status = False
        likes_count = Wishlist.objects.filter(product=product).count()

        return JsonResponse({'bool': status, 'likes_count': likes_count, 'message': 'تم الحذف'})
        # return JsonResponse({'bool': False, 'message': 'تم الحذف'})

    else:
        status = True
        return JsonResponse({'bool': status, 'likes_count': likes_count, 'message': 'لم يتم الحذف'})
        # return JsonResponse({'bool': False, 'message': 'لم يتم الحذف' })
   
# 7:C 🌸done
def wishlist_partial(request):
    wishlist_products = []
    cart_items = []
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        products = Product.objects.filter(wishlist__customer=customer)
        if customer:
            wishlist_products = Wishlist.objects.filter(customer=customer).values_list('product_id', flat=True)
            cart = Cart.objects.filter(customer=customer, is_active=True).first()
            if cart:
                # عشان اتاكد موجود في السلة ولا لا للتبديل لكل الايقونات
                cart_items = CartItem.objects.filter(cart=cart).values_list('product_id', flat=True) 
    
    context={
        'products_wishlist': products,
        'cart_items': cart_items, 
        'wishlist_products': wishlist_products,
    }
    return render(request, 'product/wishlist_items.html',context)

# 🔴 Cart Page:-
# 8:A 🌸done
@login_required(login_url='signIn')
def cart(request):
    cart_items = []
    products = []
    
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        
        if customer:
            cart = Cart.objects.filter(customer=customer, is_active=True).first()
            if cart:
                # cart_items = CartItem.objects.filter(cart=cart).values_list('product_id', flat=True)
                cart_items = CartItem.objects.filter(cart=cart).order_by('-id')
                for m in cart_items:
                    print(m)
                total_items = cart_items.count()
            else:
                total_items = 0
    # 3 random products
    random_products = Product.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('?')[:3]

    context = {
        'cart_items': cart_items,
        'total_items': total_items,
        'products': random_products, 
    }
    return render(request, "product/cart.html", context)

def cart_partial(request):
    pass
# 8:B 🌸done
@login_required(login_url='signIn')
def remove_cart(request):
    user = request.user
    try:
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'لا يوجد عميل'}, status=404)
    
    cart = Cart.objects.filter(customer=customer, is_active=True)
    if not cart.exists():
            return JsonResponse({'bool': False, 'message': 'لا يوجد سلة حالياً'})
    
    cart_item_id  = request.GET.get('product_id')
    if not cart_item_id :
        return JsonResponse({'error': 'لا يوجد id منتج'}, status=400)
    
    
    try:
        cart_item = CartItem.objects.get(pk=cart_item_id, cart__customer=customer, cart__is_active=True)
        cart_item.delete()
        return JsonResponse({'deleted': True, 'message': 'تم حذف المنتج من السلة'})
    except CartItem.DoesNotExist:
        return JsonResponse({'deleted': False, 'message': 'العنصر غير موجود أو لا يخص هذا المستخدم'})

# 8:C 🌸done
@login_required(login_url='signIn')
def update_cart_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = request.POST.get('quantity')

        try:
            item = CartItem.objects.get(id=item_id)
            item.quantity = int(quantity)
            item.save()
            return JsonResponse({'success': True})
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'العنصر غير موجود'})
    return JsonResponse({'success': False, 'error': 'طلب غير صالح'})

# 🔴 Order Page:-

# 9:A 🌸done        
@require_POST
def order_checkout(request):
    try:
        customer = Customer.objects.filter(user=request.user).first()
        if not customer:
            return JsonResponse({"error": "❌ المستخدم غير موجود!"}, status=400)
        
        cart = Cart.objects.filter(customer=customer, is_active=True).first()
        if not cart:
            return JsonResponse({"error": "❌ السلة غير موجودة!"}, status=400)

        total_price = request.POST.get('totalPrice', '0')
        description = request.POST.get('addDicTextarea', '')

        try:
            total_price_decimal = Decimal(total_price)
        except InvalidOperation:
            return JsonResponse({
                'state': 'error',
                'message': '⚠️ السعر غير صحيح!'
            }, status=400)

        order = OrderCheckout.objects.create(
            cart=cart,
            customer=customer,
            additional_description=description,
            value_bill=total_price_decimal,
        )
        cart.is_active = False
        cart.save()

        return JsonResponse({
            'state': 'success',
            'message': '✅ تم استلام الطلب بنجاح',
            'data': {
                'total_price': total_price,
                'notes': description
            }
        }, status=200)

    except Exception as e:
        import traceback
        traceback.print_exc()  # يظهر الخطأ في الطرفية
        return JsonResponse({
            'state': 'error',
            'message': f'حدث خطأ داخلي: {str(e)}'
        }, status=500)


# 9:B 🌸done
@login_required
def order(request):
    customer = Customer.objects.filter(user=request.user).first()
    if not customer:
        return render(request, "product/order.html", {"orders": []})
    # orders = OrderCheckout.objects.filter(customer=customer)
    # استثناء الطلبات التي تم استلامها
    orders = OrderCheckout.objects.filter(customer=customer).exclude(received_stats='r1')

    orders_with_btn = []
    for order in orders:
        show_btn = order.order_stats == 'o3' and order.payment_stats == 'p1'
        
        # جلب عناصر السلة المرتبطة بهذا الطلب
        cart_items = order.cart.cartitem_set.select_related('product')  # لتقليل الاستعلامات

        orders_with_btn.append({
            'order': order,
            'show_btn': show_btn,
            'cart_items': cart_items,
        })

    context = {
        'orders_with_btn': orders_with_btn
    }
    return render(request, "product/order.html", context)

# 9:C 🌸done
@csrf_exempt  
def mark_as_received(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'الطلب غير مسموح'}, status=405)

    user = request.user
    try:
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'لا يوجد عميل'}, status=404)

    order = OrderCheckout.objects.filter(customer=customer,)
    if not order.exists():
        return JsonResponse({'bool': False, 'message': 'لا يوجد طلب حالياً'})

    order_item_id = request.POST.get('order_id')
    if not order_item_id:
        return JsonResponse({'error': 'لا يوجد id للطلب'}, status=400)

    try:
        order_item = OrderCheckout.objects.get(pk=order_item_id, customer=customer)
        # ممكن تضيف تعديل هنا على حالة الاستلام:
        order_item.received_stats = 'r1'  # أو أي قيمة من choices
        order_item.save()
        return JsonResponse({'deleted': True, 'message': 'تم تأكيد استلام الطلب'})
    except OrderCheckout.DoesNotExist:
        return JsonResponse({'deleted': False, 'message': 'الطلب غير موجود أو لا يخص هذا المستخدم'})
