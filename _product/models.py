from django.db import models
from _account.models import CustomUser, Customer
from django.db.models import Avg
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="اسم الفئة")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "فئة"
        verbose_name_plural = "a_الفئات"

class SubCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name="اسم الفئة الفرعية")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="الفئة الرئيسية")

    def __str__(self):
        return f"{self.name} ({self.category.name})"
    
    class Meta:
        verbose_name = "فئة فرعية"
        verbose_name_plural = "b_ الفئات الفرعية"

class Product(models.Model):
    choices_gender = [
        ('a', 'ذكر'),
        ('b', 'أنثى'),
        ('c', 'للجنسين')
    ]
    
    choices_colors = [
        ('#FF0000', 'أحمر'),
        ('#0000FF', 'أزرق'),
        ('#FFFF00', 'أصفر'),
        ('#00FF00', 'أخضر'),
        ('#FFA500', 'برتقالي'),
        ('#800080', 'بنفسجي'),
        ('#000000', 'أسود'),
        ('#FFFFFF', 'أبيض'),
        ('#808080', 'رمادي'),
        ('#A52A2A', 'بني'),
        ('#FFC0CB', 'وردي'),
        ('#F5F5DC', 'بيج')
    ]

    choices_age_range = [
        ('a', '1-3 أشهر'),
        ('b', '4-6 أشهر'),
        ('c', '7-9 أشهر'),
        ('d', 'سنة'),
    ]


    product_name = models.CharField(max_length=255, verbose_name="اسم المنتج")
    product_description = models.TextField(blank=True, null=True, verbose_name="وصف المنتج")
    product_image = models.ImageField(upload_to='ProductsImages/%Y/%m/%d/', verbose_name="صورة المنتج")
    product_purchas_cost = models.FloatField(verbose_name="سعر الشراء")
    product_selling_price = models.FloatField(verbose_name="سعر البيع")
    product_stock_quantity = models.IntegerField(verbose_name="الكمية في المخزون")
    product_subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, verbose_name="الفئة الفرعية")
    product_age_range = models.CharField(max_length=50, choices=choices_age_range, verbose_name="الفئة العمرية", default="a")
    product_gender = models.CharField(max_length=10, choices=choices_gender, verbose_name="الجنس", default="c")
    product_color = models.CharField(max_length=10, choices=choices_colors, verbose_name="اللون", default="#FFFFFF") 
    product_created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    product_updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    product_is_active = models.BooleanField(default=True, verbose_name="متاح")

    def __str__(self):
        return self.product_name
    
    class Meta:
        verbose_name = "منتج"
        verbose_name_plural = "c_المنتجات"

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})


    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})

    def average_rating(self):
        avg_rating = Review.objects.filter(product=self).aggregate(Avg('rating'))['rating__avg']
        return round(avg_rating, 2) if avg_rating else 0  # إذا لم يكن هناك تقييمات، أعد 0

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="المنتج")
    image = models.ImageField(upload_to='ProductsImagesAdd/%Y/%m/%d/', verbose_name="الصورة")

    def __str__(self):
        return f"صورة لـ {self.product.product_name}"
    
    class Meta:
        verbose_name = "صورة منتج"
        verbose_name_plural = "d_صور المنتجات"

class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="العميل")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="المنتج")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="التاريخ")

    class Meta:
        unique_together = ('customer', 'product')  # لمنع تكرار نفس المنتج لنفس العميل

    class Meta:
        verbose_name = "مفضل"
        verbose_name_plural = "e_المفضلة"

    def __str__(self):
        return f"{self.customer.user.email} - {self.product.product_name}"

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="العميل")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الانشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")
    is_active = models.BooleanField(default=True, verbose_name="نشط؟")
    class Meta:
        verbose_name = "السلة"
        verbose_name_plural = "f_السلال"

    def __str__(self):
        return f"{self.customer.user.email} -  {'نشطة' if self.is_active else 'غير نشطة'}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="السلة")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="المنتج")
    quantity = models.PositiveIntegerField(verbose_name="الكمية")

    @property
    def total_price(self):
        return self.quantity * self.product.product_selling_price  # حساب السعر بدل تخزينه

    # total_price = models.PositiveIntegerField(verbose_name="السعر الاجمالي")
    class Meta:
        verbose_name = "عنصر السلة"
        verbose_name_plural = "f_عناصر السلة"

    def __str__(self):
        return f"{self.cart.customer.user.email} - {self.cart.created_at.date()} - {self.product.product_name}"

class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,  verbose_name="العميل")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews",  verbose_name="المنتج")  # إضافة related_name لتسهيل العلاقة
    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="تاريح الانشاء")
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)],  verbose_name="التقييم النجمي")
    comment = models.TextField(blank=True, null=True,  verbose_name="التقييم النصي")

    class Meta:
        verbose_name = " مراجعة المنتج "
        verbose_name_plural = "g_مراجعات المنتجات"

    def __str__(self):
        return f"Review by {self.customer} for {self.product} - {self.rating} stars"

# Oreder Models:-

class Delivered(models.Model):
    name = models.CharField(max_length=255,  verbose_name="اسم عامل التوصيل")
    phone = models.CharField(max_length=20,  verbose_name="رقم الهاتف")
    address = models.TextField(verbose_name="العنوان")
    created_admin = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,  verbose_name="تمت الاضافة من")
    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="تاريخ الاضافة")

    class Meta:
        verbose_name = " الموصل  "
        verbose_name_plural = "h_الموصلين"


    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)

        if not self.pk and current_user:
            if not current_user.is_staff:  # أو current_user.is_superuser حسب نوع الأدمن عندك
                raise ValueError("فقط الإدمن يمكنه إضافة عامل توصيل.")
            self.created_admin = current_user

        super().save(*args, **kwargs)

class OrderCheckout(models.Model):
    code = models.CharField(max_length=30, unique=True, blank=True, verbose_name="كود السلة المنفرد")
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, verbose_name="السلة")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', verbose_name="العميل")
    additional_description = models.TextField(null=True, blank=True, verbose_name="وصف اضافي للمنتج")
    value_bill = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="الفاتورة")
    received_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="المبلغ المدفوع")

    choices_Payment_State = [

        ('p0', 'لم يتم التسليم'),
        ('p1', 'تم التسليم'),

        
    ]
    choices_Order_State = [
        ('o0', 'قيد الانتظار'),
        ('o1', 'جار المعالجة'),
        ('o2', 'تم الشحن'),
        ('o3', 'تم التسليم'),
        ('o4', 'تم الإلغاء'),
    ]
    choices_Received_State = [
        ('r0', 'لم يتم الاستلام'),
        ('r1', 'تم الاستلام'),
    ]

    # التحكم من : updated_by (admin) اي تسجل من قام بالتعدل
    payment_stats = models.CharField(max_length=2, choices=choices_Payment_State, default='p0', verbose_name="حالة الدفع") 
    # التحكم من : updated_by (admin) اي تسجل من قام بالتعدل
    order_stats = models.CharField(max_length=2, choices=choices_Order_State, default='o0', verbose_name="حالة الشحن")      
    # التحكم من : customer اي تسجل من قام بالتعدل
    received_stats = models.CharField(max_length=2, choices=choices_Received_State, default='r0', verbose_name="حالة الاستلام") 


    updated_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='updated_orders',
         verbose_name="قام بالتعديل:"
    )
    
    
    #  التحكم من : updated_by (admin) اي تسجل من قام بالتعدل لل : delivered_by
    delivered_by = models.ForeignKey(
        Delivered, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='delivered_orders',
         verbose_name="عامل التوصيل"
    )

    def save(self, *args, **kwargs):
        # من نفّذ هذا التعديل؟ يجب تمرير المستخدم كـ kwarg
        current_user = kwargs.pop('current_user', None)

        # إذا الكود مش موجود، ننشئ كود فريد
        if not self.code:
            now = timezone.now()
            year = now.strftime('%Y')
            day = now.strftime('%m%d')
            prefix = f'ORD-{year}-{day}'
            last_order = OrderCheckout.objects.filter(code__startswith=prefix).order_by('-id').first()
            if last_order and last_order.code:
                last_number = int(last_order.code.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 10001
            self.code = f'{prefix}-{new_number}'

        # التحقق: هل التعديلات التي تمت هي من نوع "تحكم إداري"؟ 
        if current_user:
            try:
                old = OrderCheckout.objects.get(pk=self.pk)
            except OrderCheckout.DoesNotExist:
                old = None

            admin_fields_changed = False
            if old:
                if old.payment_stats != self.payment_stats:
                    admin_fields_changed = True
                if old.order_stats != self.order_stats:
                    admin_fields_changed = True
                if old.delivered_by != self.delivered_by:
                    admin_fields_changed = True
            else:
                admin_fields_changed = True  # الطلب جديد

            if admin_fields_changed:
                self.updated_by = current_user

        super().save(*args, **kwargs)


    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الانشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")

    def __str__(self):
        return f"{self.code} - {self.get_received_stats_display()}"
    
    class Meta:
        verbose_name = " الطلب  "
        verbose_name_plural = "o_الطلبات"

# python manage.py makemigrations
# python manage.py migrate