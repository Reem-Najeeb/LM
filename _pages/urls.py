from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contactUs', views.contactUs, name='contactUs'),
    path('aboutUs', views.aboutUs, name='aboutUs'),

    # 
    # path('<int:pro_id>', views.product, name='product'),
    # path('products', views.products, name='products'),
]
'''
{% url 'index' %}
{% url 'contactUs' %}
{% url 'aboutUs' %}
'''