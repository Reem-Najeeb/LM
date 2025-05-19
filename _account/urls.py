from django.urls import path
from . import views

urlpatterns = [
    # 1✔️
    path('signup', views.Sign_Up, name='signUp'),
    # 2✔️
    path('signin', views.Sign_In, name='signIn'),
    # 3✔️
    path('logout', views.Log_Out, name='logOut'),
    # 4✔️
    path('atc', views.AccounTermsConditions, name='atc'),
    
    # 5, 6, 7✔️ All 
    path('forgetPssword/', views.Forgot_Password, name='forgetPssword'),
    path('passwordResetSent/<str:reset_id>/', views.Password_Reset_Sent, name='passwordResetSent'),
    path('resetPassword/<str:reset_id>/', views.Reset_Password, name='resetPassword'),

    # 8✔️
    path('profile', views.Profile, name='profile'),  # 8✔️
    path("update-profile/", views.update_profile, name="update_profile"),  # 9✔️ (Json)
    path("update_or_create_customer/", views.update_or_create_customer, name="update_or_create_customer"),  # 10✔️ (Json)

    # ✔️ JSON 
    path('get_json_data_info_user/', views.get_json_data_info_user, name='get_json_data_info_user'),  # 11✔️ (Json)

    path('get_json_data_cities/', views.get_json_data_cities, name='get_json_data_cities'), # 12:C✔️ (Json)
    path('get_json_data_street/<int:city_id>/', views.get_json_data_street, name='get_json_data_street'), # 12:S✔️ (Json)
    path('get_json_data_info_customer/', views.get_json_data_info_customer, name='get_json_data_info_customer'),  # 13✔️ (Json)
    
    # work 14 ramadan
    path('get_json_data_baby_info/', views.get_json_data_baby_info, name='get_json_data_baby_info'), # 14:GB:✔️done: (Json)
    path('update_json_data_baby_info/', views.update_json_data_baby_info, name='update_json_data_baby_info'), # 14:UB:✔️done: (Json)
]
'''
Call Links:-
{% url 'signIn' %}
{% url 'forgetPssword' %}
{% url 'signUp' %}
{% url 'logOut' %}
{% url 'profile' %}
{% url 'atc' %}

# pass:
{% url 'forgetPssword' %}
'''