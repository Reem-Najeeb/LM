"""
Lang_ar[4]=> 
from django.conf.urls.i18n import i18n_patterns
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]
// += i18n_patterns
// رابط اللغة اساسي عشان كدة نخليه وحده
--------
[static & template]=>
from . import  settings
from django.contrib.staticfiles.urls import static
 + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
from django.contrib import admin
from django.urls import path, include

from . import  settings
from django.contrib.staticfiles.urls import static

from django.conf.urls import handler404
from django.shortcuts import render

# from .views import handler_404

from django.conf.urls.i18n import i18n_patterns

def custom_404(request, exception):
    return render(request, '404.html', status=404)

handler404 = custom_404

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('_pages.urls')),
    path('account/', include('_account.urls')),
    path('product/', include('_product.urls')),
    
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


