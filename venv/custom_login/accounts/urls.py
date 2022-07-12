from os import name
from django.urls import path
from accounts import views 

app_name = 'accounts'

urlpatterns = [
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    # path('email/confirmation/<str:activation_key>',views.email_confirm,name='email_activation'), 
    path('profile/',views.profile,name="profile"),
    path('change-password/',views.PassChange.as_view(),name="pass-change"),
    path('change-pic/',views.change_image,name="image-change"),
    path('change_general_info/',views.change_general_info,name="change_general_info")
]
