from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from properties.models import Feedback, Property
from properties.forms import PropertyAddForm

# Create your views here.

def index(request):
    obj = Property.objects.all()
    return render(request,'properties/index.html',{'property':obj})

@login_required
def add_properties(request):
    template = 'properties/add.html'
    form = PropertyAddForm()
    
    if request.method == "POST":
        form = PropertyAddForm(request.POST,files=request.FILES)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.submitted_by = request.user
            instance.save()
            return redirect('properties:index')
    
    context = {'form':form}
    return render(request,template,context)

@login_required
def edit_properties(request,pk):
    property = get_object_or_404(Property,pk=pk)
    form = PropertyAddForm(instance=property)
    
    if property.submitted_by == request.user:
        if request.method == "POST":
            form = PropertyAddForm(request.POST,files=request.FILES,instance=property)

            if form.is_valid():
                form.save()
            
            return redirect("properties:index")
        return render(request,'properties/update.html',{'form':form})
    return render(request,"properties/index.html")


@login_required
def delete_properties(request,pk):
    property = get_object_or_404(Property,pk=pk)
    
    if property.submitted_by == request.user:
        property.delete()

    return render(request,"properties/index.html")


@login_required
def feedback(request,pk):
    property = Property.objects.get(pk=pk)
    if property.submitted_by == request.user:
        x = Feedback.objects.filter(property=property)
        return render(request,'properties/feedbacks.html',{'x':x})

@login_required
def feedbacks(request):
    feedbacks = Feedback.objects.filter(property__submitted_by=request.user)

    if feedbacks:
        return render(request,'properties/feedbacks.html',{'feedbacks':feedbacks})
    
    else:
        return render(request,'properties/feedbacks.html',{'msg':"No Feedback Right Now"})
    