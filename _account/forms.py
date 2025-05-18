from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, City, Street, Customer, CustomerBaby
# , CustomerBaby
from django.contrib.auth import authenticate, get_user_model

# 
# forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تأكيد كلمة المرور', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone_number')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("كلمتا المرور غير متطابقتين")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomUserChangeForm(forms.ModelForm):
    password = forms.CharField(label="كلمة المرور", widget=forms.PasswordInput, required=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_staff')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # المستخدم الذي يتم تعديله
        user_being_edited = self.instance

        if user_being_edited and not user_being_edited.is_staff:
            self.fields['password'].disabled = True
            self.fields['password'].help_text = "لا يمكن تعديل كلمة المرور لهذا المستخدم (ليس موظفًا)."
        else:
            self.fields['password'].help_text = "أدخل كلمة مرور جديدة لتحديثها، أو اتركها فارغة لعدم التغيير."

    def save(self, commit=True):
        user = super().save(commit=False)
        if not self.fields['password'].disabled:
            password = self.cleaned_data.get('password')
            if password:
                user.set_password(password)
        if commit:
            user.save()
        return user

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "id":"firstName", "placeholder": "الاسم الأول"})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "id":"lastName", "placeholder": "العائلة"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control en",  "id":"email","placeholder": "email@gmail.com"})
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "id":"phone",
            "placeholder": "7xx xxx xxx",
            "pattern": "[7-9][0-9]{8}",
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control en border-0",
            "id":"password",
            "placeholder": "********",
            "oninput": "restrictToEnglish(event, 'englishInput')"
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control en border-0",
            "id":"confirm-password",
            "placeholder": "********",
            "oninput": "restrictToEnglish(event, 'englishInput')"
        })
    )
    
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2']

User = get_user_model()
class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class":"en form-control",
            "id":"email",
            "placeholder":"email@gmail.com",
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "id":"password",
            "class":"en form-control border-0",
            "placeholder":"********",
            "oninput":"restrictToEnglish(event, 'englishInput')",
        })
    )
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            user = authenticate(username=email, password=password)  # Django يتطلب username، لكنك تستخدم email
            
            if user is None:
                raise forms.ValidationError("البريد الإلكتروني أو كلمة المرور غير صحيحة!")
        
        return self.cleaned_data

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [ 'street', 'address', 'additional_phone']

# class CustomerBabyInfoForm(forms.ModelForm):
#     class Meta:
#         model = CustomerBaby
#         fields = [ 'baby_name',
#                    'baby_birthday', 
#                    'baby_gender', 
#                    'baby_picture']

#     class Meta:
#         model = Customer
#         fields = '__all__'
#         widgets = { 
#             # 'name': forms.TextInput(attrs={ 'class': 'form-control' }), 
#             'street': forms.Select(attrs={ 'class': 'form-select' }),
#             # 'city': forms.Select(attrs={ 'class': 'form-select' }),
#             'address': forms.TextInput(attrs={ 'class': 'form-control' }), 
#             'additional_phone': forms.EmailInput(attrs={ 'class': 'form-control' }),
#         }    
 
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['city'].queryset = City.objects.none()
 
#         if 'city' in self.data:
#             try:
#                 city_id = int(self.data.get('city'))
#                 self.fields['street'].queryset = Street.objects.filter(city_id=city_id).order_by('name')
#             except (ValueError, TypeError):
#                 pass  # invalid input from the client; ignore and fallback to empty City queryset
#         elif self.instance.pk:
#             self.fields['street'].queryset = self.instance.city.city_set.order_by('name')
