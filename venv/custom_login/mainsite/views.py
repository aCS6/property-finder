from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from properties.models import City, Property,Status,Feedback
from mainsite.models import OurServices, Testimonial,AboutUs
from blog.models import Blog
from django.contrib.auth import get_user_model



User = get_user_model()
# Create your views here.

def index(request):
    property_list = Property.objects.only("title","address","city","status","area","area_unit","price","bedroom","bathroom","garage","image1").order_by('-submission_date').filter(is_published=True)
    
    services = OurServices.objects.all()
    latest_blog = Blog.objects.all().order_by("-publish_date")[:3]
    testimonial = Testimonial.objects.all()

    status = Status.objects.all()
    city = City.objects.all()

    context = {
        'property':property_list,
        'services': services,
        'blog' :latest_blog,
        'testimonial':testimonial,
        'search_status':status,
        'search_city':city
    }
    return render(request,'mainsite/index.html',context)

def single_property(request, pk):
    property = Property.objects.get(pk=pk)
    
    if property is not None:
        context = {
            'property':property,
        }

        if request.method == "POST":
            if request.POST.get('feedbackEmail') and request.POST.get('feedbackName') and request.POST.get('feedbackText'):
                name = request.POST.get('feedbackName')
                email = request.POST.get('feedbackEmail')
                text = request.POST.get('feedbackText')
                property = property.id
                
                try:
                    obj = Feedback(property_id = property,name=name,email=email,comment=text)
                    obj.save()

                    context['send_feedback_ok'] = 'Thanks for your feedback.'
                    return render(request,'mainsite/single_property.html',context)
                except:
                    context['send_feedback_ok'] = 'Something wrong! Please Check Properly'

                
    else:
        context={}
    return render(request,'mainsite/single_property.html',context)


def agent_single(request,pk):
    obj = get_object_or_404(User,pk=pk)

    return render(request,"mainsite/individual_property.html",{'obj':obj})

def all_property(request):
    obj = Property.objects.all()
    return render(request,"mainsite/all_property.html",{'obj':obj})

def navbar(request,status):
    obj = Property.objects.all().filter(status__name=status)

    if obj:
        context ={
            'obj':obj,
            'status':status,
        }
        return render(request,'mainsite/status_property.html',context)
    else:
        msg = f"No Properties for {status} right now! Coming soon..."
        return render(request,'mainsite/status_property.html',{'msg':msg})

def navbar_navigation(request,status,type):
    obj = Property.objects.all().filter(status__name=status,property_type__name=type)

    if obj:
        context ={
            'obj':obj,
            'status':status,
            'type':type
        }
        return render(request,'mainsite/navigation.html',context)
    else:
        msg = f"No {type} for {status} right now! Coming soon..."
        return render(request,'mainsite/navigation.html',{'msg':msg})
        

def search(request):

    obj = Property.objects.all().order_by('-submission_date')

    if 'keywords' in request.POST:
        keywords = request.POST.get('keywords')
        if keywords:
            obj = obj.filter(description__icontains=keywords)

    # Status
    if 'status' in request.POST:
        if request.POST.get('status') != "All Type":
            status = request.POST.get('status')
            if status:
                obj = obj.filter(status__name__iexact=status)
                

    if 'city' in request.POST:
        if request.POST.get('city') != "All City":
            city = request.POST.get('city')
            if city:
                obj = obj.filter(city__name__iexact=city)
                

    return render(request,'mainsite/search.html',{'obj':obj})

def about(request):
    about = AboutUs.objects.get(pk=1)

    return render(request,'mainsite/about.html',{'about':about})