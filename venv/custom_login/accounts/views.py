from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render,redirect,get_object_or_404
from django.template.loader import render_to_string
from accounts.forms import UserRegistrationForm,UserLoginForm,ExtraInfoChange,ExtraInfoChange2,UserInfoChange
from django.contrib.auth import login,logout,get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from accounts.models import EmailConfirmed,ExtraInfo,CustomUser
from properties.models import Property
from blog.models import Blog
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.urls import reverse



User = get_user_model()
# Create your views here.

def register_view(request):
    form = UserRegistrationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            instance = form.save(commit=False)
            #instance.is_active = False
            instance.save()

            ext = ExtraInfo(user=instance)
            ext.save()
            # send mail
            # user = EmailConfirmed.objects.get(user=instance)
            # site = get_current_site(request)
            # email = instance.email
            # first_name = instance.first_name
            # last_name = instance.last_name
            # email_body = render_to_string(
            #     'accounts/verify_email.html',
            #     {
            #         'first_name' : first_name,
            #         'last_name':last_name,
            #         'email' : email,
            #         'domain':site.domain,
            #         'activation_key': user.activation_key
            #     }
            # )
            # send_mail(
            #     subject='Email Confirmation',
            #     message = email_body,
            #     from_email='amir16101006@gmail.com',
            #     recipient_list=[email],
            #     fail_silently= True
            # )
            # return render(request,'accounts/registration_start.html')
            return render(request,'accounts/registration_complete.html')
        
        return render(request,'accounts/register.html',{'form':form})
    
    return render(request,'accounts/register.html',{'form':form})

def login_view(request):
    _next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user_obj = form.cleaned_data.get('user_obj')
            login(request,user_obj)

            if _next:
                return redirect(_next)
            
            return redirect('pages:index')
        
        return render(request,'accounts/login.html',{'form':form})
    return render(request,'accounts/login.html',{'form':form})

@login_required(login_url='accounts:login')
def logout_view(request):
    logout(request)
    return redirect("accounts:login")

@login_required
def profile(request):
    info1 = CustomUser.objects.get(email=request.user)
    info2 = ExtraInfo.objects.filter(user=request.user)
    total_property = Property.objects.filter(submitted_by=request.user).count()
    total_blog = Blog.objects.filter(author=request.user).count()

    

    context ={
        'info1':info1,
        'info2':info2,
        'total_property':total_property,
        'total_blog':total_blog
    }

    return render(request,'accounts/profile.html',context)
# def email_confirm(request,activation_key):
#     user = get_object_or_404(EmailConfirmed,activation_key=activation_key)
#     if user is not None:
#         user.email_confirmed = True
#         user.save()

#         instance = User.objects.get(email=user)
#         instance.is_active = True
#         instance.save()

#         return render(request,'accounts/registration_complete.html')

class PassChange(PasswordChangeView):
    template_name = 'accounts/pass_change.html'
    success_url = reverse_lazy('accounts:profile')




@login_required
def change_image(request):
    obj = get_object_or_404(ExtraInfo,user=request.user)

    form = ExtraInfoChange(instance=obj)

    if request.method == "POST":
        form = ExtraInfoChange(request.POST,files=request.FILES,instance=obj)

        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect(reverse('accounts:profile'))
            
        return render(request,'accounts/profile.html')
    
    return render(request,"accounts/change_profile.html",{'form':form})


@login_required
def change_general_info(request):
    obj = get_object_or_404(ExtraInfo,user=request.user)
    
    form2 = ExtraInfoChange2(instance=obj)

    if request.method == "POST":
        form2 = ExtraInfoChange2(request.POST,instance=obj)

        if form2.is_valid():
            form2.save()
            
            return HttpResponseRedirect(reverse('accounts:profile'))

            
        return render(request,'accounts/profile.html')
    
    return render(request,"accounts/change_general_info.html",{'form2':form2})
