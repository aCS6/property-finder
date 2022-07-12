from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.forms import fields
from accounts.models import ExtraInfo

User = get_user_model()

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','first_name','last_name')
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 !=password2:
            raise forms.ValidationError("Password don't match")
        
        return password2
    
    def save(self,commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))

        if commit:
            user.save()
        
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email','password','first_name','last_name','is_active','is_staff','is_admin')

        def clean_password(self):
            return self.initial['password'] 
            # password change korar somoy ager password dekhabe ( read only hash akare)

class UserRegistrationForm(UserCreationForm):
    
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'type':'email',
                'placeholder':'Enter Your Email'
            }
        )
    )

    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Enter First Name'
            }
        )
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Enter Last Name'
            }
        )
    )

    password1 = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'type':'password',
                'placeholder':'Enter a Password'
            }
        )
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'type':'password',
                'placeholder':'Retype Password'
            }
        )
    )

    class Meta:
        '''Meta Class'''
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2'
        ]

    def clean_email(self):
        error_messages = {
            'duplicate_email' : 'Email is already Taken'
        }

        email = self.cleaned_data.get('email')

        try:
            User.objects.get(email=email)

            raise forms.ValidationError(
                error_messages['duplicate_email'],
                code='duplicate_email',
            )
        
        except User.DoesNotExist:
            return email


class UserLoginForm(forms.Form):
    
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'type':'email',
                'placeholder':'Enter Your Email',
                'required': True
            }
        )
    )

    password = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'type':'password',
                'placeholder':'Enter Your Password',
                'required': True
            }
        )
    )

    def clean(self,*args,**kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        user_qs_final = User.objects.filter(Q(email__iexact = email)).distinct()

        if not user_qs_final.exists() and user_qs_final.count !=1:
            raise forms.ValidationError("User does not exist")
        
        user_obj = user_qs_final.first()

        if not user_obj.check_password(password):
            raise forms.ValidationError("Credentials are not Correct")
        
        self.cleaned_data["user_obj"] = user_obj

        return super(UserLoginForm,self).clean(*args,**kwargs)


class ExtraInfoChange(forms.ModelForm):
    class Meta:
        model = ExtraInfo
        fields = [
            "profile_pic",
        ]

class ExtraInfoChange2(forms.ModelForm):
    class Meta:
        model = ExtraInfo
        fields = [
            "phone_number1",
            "phone_number2",
            "about_me"
        ]

class UserInfoChange(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name')

