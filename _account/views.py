from datetime import datetime
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required # @login_required
# from django.contrib.auth.models import User

from .forms import SignUpForm, LoginForm
# CustomerBabyInfoForm
# from .models import CustomUser, CustomerBaby, PasswordReset, City, Street
from .models import *
import socket
from django.urls import reverse
from django.core.mail import EmailMessage
from django.utils import timezone
from django.contrib import messages


from django.utils.timezone import now
import uuid
import logging


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import CustomUser

'''Main Account Functions:-'''
# 1🌸done:
def Sign_Up(request):
    form = SignUpForm()  
    if request.user.is_authenticated and not request.user.is_anonymous:
            return redirect("profile")  

    if request.method == "POST":
        form = SignUpForm(request.POST)  
        if form.is_valid():  
            user = form.save()  
            login(request, user)
            return redirect("profile")  
        else:
            messages.error(request, 'هناك خطأ في البيانات المدخلة، يرج التحقق.')  
    context = {
        "form": form  
    }
    return render(request, 'account/signUp.html', context)

# 2🌸done:
def Sign_In(request):
    if request.user.is_authenticated and not request.user.is_anonymous:
            return redirect("profile")  
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "تم تسجيل الدخول بنجاح!")
                return redirect("index")
            else:
                messages.error(request, "البريد الإلكتروني أو كلمة المرور غير صحيحة!")
                return redirect("signIn") 
        else:
            messages.error(request, "البريد الإلكتروني أو كلمة المرور غير صحيحة!")

            return redirect("signIn") 
    else:
        form = LoginForm()

    context = {"form": form}
    return render(request, "account/signIn.html", context)


# 3🌸done:
def Log_Out(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('index')
    else:
        return redirect('index')

# 4🌸done:
def AccounTermsConditions(request):
    return render(request , 'account/atc.html')

'''Reset Password Functions:-'''
# 5🌸done:
def Forgot_Password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()
            password_reset_url = reverse('resetPassword', kwargs={'reset_id': new_password_reset.reset_id})
            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'
            email_body = f'ادخل البريد:\n\n{full_password_reset_url}'
            email_message = EmailMessage(
                'Reset your password',  
                email_body,  
                settings.EMAIL_HOST_USER,  
                [email]  
            )
            email_message.fail_silently = True
            
            try:
                email_message.send()
            except (socket.gaierror, ConnectionResetError) as e:
                messages.error(request, 'لديك مشكلة في الانترنت...')
                return redirect('forgetPssword')

            return redirect('passwordResetSent', reset_id=new_password_reset.reset_id)

        except CustomUser.DoesNotExist:
            messages.error(request, f"البريد الالكتروني هذا غير متوفر:{email} ")
            return redirect('forgetPssword')
    return render(request, 'account/password/forgot_password.html')

# 6🌸done:
def Password_Reset_Sent(request, reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'account/password/password_reset_sent.html')
    else:
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')

# 7🌸done:
def Reset_Password(request, reset_id):
    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)
        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            passwords_have_error = False

            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')

            if len(password) < 5:
                passwords_have_error = True
                messages.error(request, 'Password must be at least 5 characters long')

            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=10)
            if timezone.now() > expiration_time:
                passwords_have_error = True
                messages.error(request, 'Reset link has expired')
                password_reset_id.delete()

            if not passwords_have_error:
                user = password_reset_id.user
                user.set_password(password)
                user.save()

                password_reset_id.delete()

                messages.success(request, 'Password reset. Proceed to login')
                return redirect('signIn')
            else:
                return redirect('resetPassword', reset_id=reset_id)
    except PasswordReset.DoesNotExist:
        messages.error(request, 'Invalid reset id')
        return redirect('forgetPssword')

    return render(request, 'account/password/reset_password.html')

'''Profile Page Functions:-'''
# 8🌸done:
def Profile(request):
    if not request.user.is_authenticated: return redirect('signIn')
    elif  request.user.is_anonymous: return redirect('signIn')
    else: print('Normal🛑')
    return render(request, 'account/profile.html')

# 9🌸done: (Json)
@login_required
@csrf_exempt
def update_profile(request):
    if request.method == "POST":
        user = request.user  
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone_number")

        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.save()

        return JsonResponse({
                'status': 'success',  
                }, status=200)
    return JsonResponse({"status": "error"}, status=400)

# 10🌸done: (Json)
@login_required
@csrf_exempt
def update_or_create_customer(request):
    if request.method == "POST":
        user = request.user
        customer, created = Customer.objects.get_or_create(user=user)
        city_id = request.POST.get("city")
        street_id = request.POST.get("street")

        try:
            if city_id:
                customer.city = City.objects.get(id=city_id)
        except City.DoesNotExist:
            customer.city = None
        try:
            if street_id:
                customer.street = Street.objects.get(id=street_id)
        except Street.DoesNotExist:
            customer.street = None

        customer.address = request.POST.get("address", "").strip()
        customer.additional_phone = request.POST.get("additional_phone", "").strip()
        
        customer.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)

# 11🌸done: (Json)
@login_required
def get_json_data_info_user(request):
    user = request.user
    user_data = {
        "first_name": user.first_name or "",
        "last_name": user.last_name or "",
        "phone_number": user.phone_number or "",
        "email": user.email or "",
    }
    return JsonResponse({"user": user_data})

# 12:C:Get Cities🌸done: (Json)
@login_required
def get_json_data_cities(request):
    qs_value = list(City.objects.values())
    return JsonResponse({'qs_value': qs_value})

# 12:S:Get Street depended on city🌸done: (Json)
@login_required
def get_json_data_street(request, *args, **kwargs):
    selectedCity = kwargs.get('city_id')
    obj_street = list(Street.objects.filter(city__id=selectedCity).values())
    return JsonResponse({'obj_street': obj_street})

# 13🌸done: (Json)
@login_required
def get_json_data_info_customer(request):
    user = request.user
    customer = get_object_or_404(Customer, user=user)
    customer_data = {
        "city": {"id": customer.city.id, "name": customer.city.name} if customer.city else None,
        "street": {"id": customer.street.id, "name": customer.street.name} if customer.street else None,
        "address": customer.address or "",
        "additional_phone": customer.additional_phone or "",
    }
    return JsonResponse({"customer": customer_data})

# 14:GB:Get Baby Info🌸done: (Json)
@login_required
def get_json_data_baby_info(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "المستخدم غير مسجل دخول"}, status=401)
    
    user = request.user
    customer = Customer.objects.filter(user=user).first()
    if not customer or not hasattr(customer, "baby"):
        return JsonResponse({"status": "error", "message": "الطفل غير موجود"}, status=404)

    baby = customer.baby
    baby_data = {
        "baby_name": baby.baby_name,
        "baby_birthday": baby.baby_birthday.strftime("%Y-%m-%d") if baby.baby_birthday else "",
        "baby_gender": baby.baby_gender,
        "baby_picture": baby.baby_picture.url if baby.baby_picture else None,
    }
    return JsonResponse({"status": "success", "baby": baby_data})

# 14:UB:Update Baby Info🌸done: (Json)
@login_required
def update_json_data_baby_info(request):
    if request.method == "POST":
        user = request.user
        customer = Customer.objects.filter(user=user).first()
        if not customer:
            messages.error(request, "لم يتم العثور على بيانات العميل.")
            return JsonResponse({"status": "error", "message": "No customer found"}, status=400)

        baby, created = CustomerBaby.objects.get_or_create(customer=customer, defaults={
            "baby_name": request.POST.get("baby_name_input", "غير معروف"),
            "baby_birthday": request.POST.get("baby_birthday_input", None),
            "baby_gender": request.POST.get("baby_gender_input", "غير محدد"),
        })

        baby_name = request.POST.get("baby_name_input")
        baby_birthday = request.POST.get("baby_birthday_input")
        baby_gender = request.POST.get("baby_gender_input")
        baby_picture = request.FILES.get("baby_picture_input")

        if baby_name: baby.baby_name = baby_name
        if baby_birthday: baby.baby_birthday = baby_birthday
        if baby_gender: baby.baby_gender = baby_gender
        if baby_picture: baby.baby_picture = baby_picture
        baby.save()

        if created:
            return JsonResponse({'status': 'success',  'message': '  تم إنشاء بيانات الطفل بنجاح. ',}, status=200)
        else:
            return JsonResponse({'status': 'success',  'message': 'تم تحديث بيانات الطفل بنجاح!',}, status=200)

    messages.error(request, "طلب غير صالح.")
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

'''End'''