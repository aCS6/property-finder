from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from datetime import datetime
import hashlib

from django.utils.translation import activate

# Creating a Model Manager
class CustomUserManager(BaseUserManager):
    # Two things to be defined. 
    # 1) Normal User Creation
    # 2) Super User Creation

    def create_user(self,email,first_name,last_name,password=None):
        if not email:
            raise ValueError('User Must Have An Email')
        
        email = email.lower()
        first_name = first_name.title()
        last_name = last_name.title()

        user = self.model(
            email = self.normalize_email(email), # convention
            first_name = first_name,
            last_name = last_name
        )
        
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,first_name,last_name,password=None):
        # first creating user
        user = self.create_user(
            email= email,
            first_name = first_name,
            last_name= last_name,
            password= password
        )

        # special for superuser
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=200,unique=True, verbose_name="email")
    first_name = models.CharField(max_length=150,verbose_name='first_name')
    last_name = models.CharField(max_length=150,verbose_name='last_name')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email' # email as a username
    REQUIRED_FIELDS = ('first_name','last_name')

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email
    
    # These methods for custom user (must be)

    def get_short_name(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return self.is_admin
    
    class Meta:
        verbose_name_plural = 'Users'

class ExtraInfo(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name="user_extra")
    profile_pic = models.ImageField(upload_to='profile_pic',null=True,blank=True)
    phone_number1 = models.CharField(max_length=15, null=True,blank=True)
    phone_number2 = models.CharField(max_length=15,null=True,blank=True)
    about_me = models.TextField(null=True,blank=True)

    def __str__(self) -> str:
        return self.user.first_name+" "+self.user.last_name+"'s Info"


class EmailConfirmed(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=500)
    email_confirmed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add = True)

    def __str__(self) -> str:
        return self.user.email
    
    class Meta:
        verbose_name_plural = 'User Email-Confirmed'


# @receiver(post_save,sender=CustomUser)
# def create_user_email_confirmation(sender,instance,created,**kwargs):
#     if created:
#         dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         email_confirmed_instance = EmailConfirmed(user=instance)
#         user_encoded = f'{instance.email}-{dt}'.encode()
#         activation_key = hashlib.sha224(user_encoded).hexdigest()
#         email_confirmed_instance.activation_key = activation_key
#         email_confirmed_instance.save()