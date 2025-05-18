from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(Category)
# admin.site.register(SubCategory)

# admin.site.register(Product)
# admin.site.register(ProductImage)

class ProductImageInline(admin.TabularInline):  # عرض عناصر السلة داخل صفحة السلة
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    model = Product  # فلترة حسب النشاط والتاريخ
    inlines = [ProductImageInline]  # عرض عناصر السلة داخل صفحة السلة

admin.site.register(Product, ProductAdmin)

admin.site.register(Wishlist)


class SubCategoryInline(admin.TabularInline):  # عرض عناصر السلة داخل صفحة السلة
    model = SubCategory
    extra = 0  # عدد الحقول الفارغة عند الإضافة

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )  # الأعمدة في القائمة
    inlines = [SubCategoryInline]  # عرض عناصر السلة داخل صفحة السلة

admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory)

# admin.site.register(Cart)
# admin.site.register(CartItem)


class CartItemInline(admin.TabularInline):  # عرض عناصر السلة داخل صفحة السلة
    model = CartItem
    extra = 1  # عدد الحقول الفارغة عند الإضافة

class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_at', 'updated_at', 'is_active')  # الأعمدة في القائمة
    search_fields = ('customer__user__email',)  # البحث باستخدام البريد الإلكتروني
    list_filter = ('is_active', 'created_at')  # فلترة حسب النشاط والتاريخ
    inlines = [CartItemInline]  # عرض عناصر السلة داخل صفحة السلة

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'total_price')
    search_fields = ('product__product_name',)
    list_filter = ('cart__customer',)

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'created_at', 'rating', 'comment')
    search_fields = ('product__product_name',)
    list_filter = ('customer',)
admin.site.register(Review, ReviewAdmin)


# Order:-
# admin.site.register(OrderCheckout)

@admin.register(OrderCheckout)
class OrderCheckoutAdmin(admin.ModelAdmin):
    readonly_fields = ('code', 'updated_by',) 
    def save_model(self, request, obj, form, change):
        obj.save(current_user=request.user)
        
        # نمرر المستخدم الحالي إلى دالة save()
    # اضيفي الادمن لايمكنه اضافة اوردر فقط قرائة الاوردرات على شكل جدول .



admin.site.register(Delivered)
