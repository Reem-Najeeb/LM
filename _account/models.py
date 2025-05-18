from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User
from django.db import models
from datetime import timedelta
from django.utils.timezone import now
import uuid

# الدولة
class City(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "مدينة"
        verbose_name_plural = "المدن"

# الشارع
class Street(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="streets")

    def __str__(self):
        return f"{self.name} ({self.city.name})"
    
    class Meta:
        verbose_name = "شارع"
        verbose_name_plural = "الشوارع"

# مدير المستخدم 
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("يجب إدخال البريد الإلكتروني")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

# تعديل المستخدم
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    # city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "مستخدم"
        verbose_name_plural = "المستخدمين"

# تعيين كلمة المرور
class PasswordReset(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="password_resets")
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for:({self.user.email}) at ({self.created_when})"
   
# بروفايل العميل
class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name="المستخدم")
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="المحافظة")
    street = models.ForeignKey(Street, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الشارع")
    address = models.CharField(max_length=500, blank=True, null=True, verbose_name="العنوان")
    additional_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="رقم اضافي")

    def __str__(self):
        return f"بروفايل {self.user.first_name} {self.user.last_name}"
    
    class Meta:
        verbose_name = "عميل"
        verbose_name_plural = "العملاء"


class CustomerBaby(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="baby")
    baby_name = models.CharField(max_length=255, null=False, blank=False)
    baby_birthday = models.DateField(null=False, blank=False)
    baby_gender = models.CharField(max_length=1, choices=[("0", "ذكر"), ("1", "أنثى")], null=False, blank=False)
    baby_picture = models.ImageField(upload_to="customer_baby_pictures/", null=True, blank=True,  max_length=500)

    def __str__(self):
        return f"{self.baby_name} - {self.customer.user.email}"
    
    class Meta:
        verbose_name = "طفل"
        verbose_name_plural = "اطفال"
