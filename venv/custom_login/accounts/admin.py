from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from accounts.forms import UserCreationForm, UserChangeForm
from accounts.models import ExtraInfo
# from accounts.models import EmailConfirmed

user = get_user_model()
# group must be unregister
admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm

    list_display = ('email','first_name','last_name','is_active','is_admin','is_staff')
    list_filter =('is_admin',)

    fieldsets =(
        (
            None,{
                'fields':('email','first_name','last_name','password')
            }
        ),
        (
            'Permissions',{
                'fields':('is_active','is_staff','is_admin')
            }
        )
    )

    add_fieldsets = (
        (
            None,{
                'fields':('email','first_name','last_name','is_active','password1','password2')
            }
        ),
        (
            'Permissions',{
                'fields':('is_active','is_staff','is_admin')
            }
        )
    )

    ordering = ('email',)
    search_fields = ('email',)
    filter_horizontal = ()

admin.site.register(user,UserAdmin)
admin.site.register(ExtraInfo)
# class EmailConfirmedAdmin(admin.ModelAdmin):
#     '''class docstring'''
#     list_display =(
#         'user',
#         'first_name',
#         'last_name',
#         'activation_key',
#         'email_confirmed'
#     )

#     def first_name(self,obj):
#         return obj.user.first_name

#     def last_name(self,obj):
#         return obj.user.last_name

# admin.site.register(EmailConfirmed,EmailConfirmedAdmin)
