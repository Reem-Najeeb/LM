from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *

# Register your models here.
# admin.site.register(CustomUser)

admin.site.register(Street)
admin.site.register(City)
# admin.site.register(Customer)
admin.site.register(CustomerBaby)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'city', 'street', 'address', 'additional_phone',) 
    

class CustomerInline(admin.TabularInline):  
    model = Customer
    readonly_fields = ('user', 'city', 'street', 'address', 'additional_phone',) 

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('البريد', 'الاسم الاول', 'الاسم الثاني', 'موظف')

    search_fields = ('email',)
    ordering = ('email',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('email',)
        return ()

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'is_staff')

    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('email',)
        return ()
    inlines = [CustomerInline]


