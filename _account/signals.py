
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Customer

@receiver(post_save, sender=CustomUser)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_customer_profile(sender, instance, **kwargs):
    instance.customer.save()




















'''
### **📌 خوارزمية إنشاء بروفايل العميل تلقائيًا عند تسجيل مستخدم جديد**  

#### **المدخلات:**
- نموذج المستخدم (`CustomUser`).
- نموذج العميل (`Customer`).

#### **الخطوات:**
1. **إنشاء ملف الإشارات (`signals.py`)** داخل التطبيق.
2. **استخدام إشارة `post_save`** لمراقبة أي عملية حفظ (`save()`) تحدث على نموذج المستخدم (`CustomUser`).
3. عند **إنشاء مستخدم جديد لأول مرة (`created=True`)**:
   - **إنشاء بروفايل جديد (`Customer`)** مرتبط بالمستخدم.
4. عند **تحديث المستخدم لاحقًا**:
   - **حفظ التعديلات في بروفايله تلقائيًا**.
5. **تسجيل الإشارات في `apps.py`** لضمان تشغيلها عند بدء تشغيل التطبيق.
6. **إعادة تشغيل السيرفر** وتحديث قاعدة البيانات (`migrate`) لتفعيل التغييرات.
7. **اختبار العملية** من خلال تسجيل مستخدم جديد، ثم التأكد من إنشاء البروفايل تلقائيًا.

#### **المخرجات:**
✅ عند تسجيل مستخدم جديد، يتم إنشاء بروفايل له في قاعدة البيانات تلقائيًا.
'''