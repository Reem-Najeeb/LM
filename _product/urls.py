from django.urls import path
from . import views

urlpatterns = [
    
    # 0 🔴 All Products Page:-
    # 0:A: All Products ✔️
    path('products', views.Products_List, name='Products_List'),
    # 0:B: ✔️(Json)
    path('load_more', views.Load_More,name='load_more'), # (json)


    # 2: filter Age ✔️
    path('age-filter/<str:age>/', views.Products_from_Link_age, name='Products_Links_age'),
    # 2: filter gender ✔️
    path('gender-filter/<str:gender>/', views.Products_from_Link_gender, name='Products_Links_gender'),
    # 2: filter category ✔️
    path('category-filter/<str:category_name>/', views.Products_from_Link_category, name='Products_Links_category'),
    # 2: filter best rate ✔️
    path('products/best_rate', views.bestRateProducts, name='best_rate_products'),
    # 2: filter new arrival ✔️
    path('products/new_arrival', views.newArrivalProducts, name='new_arrival_products'),
    
    # 3: search ✔️
    path('products/', views.searchProducts, name='search_products'),



    # 4: counts WishList and Cart ✔️ (product(s))
    path("wishlistCount", views.wishlist_count, name="wishlist_count"), # (json)    
    path("cartItemCount", views.cartItem_count, name="cartItem_count"), # (json)
    
    # 5: add or remove from WishList or Cart ✔️ (product(s))
    path("wishlist_ar", views.Add_or_remove_Wishlist, name="Add_or_remove_Wishlist"), # (json)
    path("single_cartItem_ar", views.Add_or_Remove_Single_CartItem, name="Add_or_Remove_Single_CartItem"), # (json)
    
    
    # 6: 🔴 single Product:-
    path('products/<int:pk>/', views.Product_Detail, name='Product_Detail'),

    path('products/<int:pk>/wishlist/', views.Add_or_remove_Wishlist_PD, name='wishlist_ar_pd'),

    path('products/<int:product_id>/add-to-cart/', views.add_to_cart_product, name='add_to_cart'),
    path('products/<int:product_id>/add-review/', views.add_review_product, name='add-review'),



    # cart and wishList 
    # 7: 🔴 WishList:-
    path('products/wishlist', views.wishlist, name='wishlist'),
    path('products/remove_Wishlist', views.remove_Wishlist, name="Add_or_remove_Wishlist"), # json
    path('products/wishlist_partial', views.wishlist_partial, name="wishlist_partial"), # json


    # 8: 🔴 Cart:-
    path('products/cart', views.cart, name='cart'),
    path('products/remove_cart', views.remove_cart, name='remove_cart'), # json
    path('products/cart/update-cart-item/', views.update_cart_item, name='update_cart_item'), # json
    # path('products/cart_partial', views.cart_partial, name="cart_partial"), # json

    # 9: 🔴 Order:-
    path('products/order_checkout', views.order_checkout, name='order_checkout'),
    path('products/order', views.order, name='order'),
    path('products/mark_received', views.mark_as_received, name='mark-received'),
]
'''
{% url 'Products_List' %}
{% url 'Product_Detail' %}
{% url 'wishlist' %}
{% url 'cart' %}
{% url 'wishlist' %}
{% url 'order' %}
'''