from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from accounts.models import CustomUser

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=80,unique=True)

    def __str__(self) -> str:
        return self.name


class Usage(models.Model):
    name = models.CharField(max_length=80,unique=True)

    def __str__(self) -> str:
        return self.name

class Property_type(models.Model):
    name = models.CharField(max_length=80,unique=True)

    def __str__(self) -> str:
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=80,unique=True)

    def __str__(self) -> str:
        return self.name

class Area_unit(models.Model):
    name = models.CharField(max_length=80,unique=True)

    def __str__(self) -> str:
        return self.name
 
    
class Property(models.Model):
    submitted_by = models.ForeignKey(CustomUser,on_delete=CASCADE,related_name="user_property")
    title = models.CharField(max_length=300,verbose_name="Give Your Property Title")
    address = models.CharField(max_length=500, verbose_name="Give Your Address")
    city = models.ForeignKey(City, on_delete=DO_NOTHING, verbose_name="City")
    usage = models.ForeignKey(Usage, on_delete=DO_NOTHING,verbose_name="Usage")
    property_type = models.ForeignKey(Property_type, on_delete=DO_NOTHING,verbose_name="Property Type")
    status = models.ForeignKey(Status, on_delete=DO_NOTHING,verbose_name="Status")
    area = models.IntegerField(verbose_name="Area in Number")
    area_unit = models.ForeignKey(Area_unit, on_delete=DO_NOTHING,verbose_name="Area Unit")
    description = models.TextField(blank=True,verbose_name="Write Some Description")
    price = models.IntegerField(blank=True,null=True,verbose_name="Property Price")
    bedroom = models.IntegerField(verbose_name="Number of Bedroom ?")
    bathroom = models.IntegerField(verbose_name="Number of Bathroom ?")
    garage = models.IntegerField(default=0,verbose_name="Number of Garage ?")
    kitchen = models.IntegerField(verbose_name="Number of kitchen")
    image1 = models.ImageField(upload_to='property/%Y/%m/%d/',verbose_name="First Image")
    image2 = models.ImageField(upload_to='property/%Y/%m/%d/',verbose_name="Second Image")
    amenities = models.TextField(verbose_name="Facities [Comma Separated]",null=True,blank=True)
    video_link = models. URLField(verbose_name="Embeded Video Link",null=True,blank=True)
    map = models.URLField(verbose_name="Embeded Map Link",null=True,blank=True)
    floor_plan = models.ImageField(upload_to='property/floor_plan/%Y/%m/%d/', verbose_name="Give Your Floor Plan", null=True,blank=True)
    established_date = models.DateField(verbose_name="Established Date",null=True,blank=True)
    publish_price = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    submission_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title.upper()

class Feedback(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_feedback')
    name = models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(max_length=50)
    comment = models.TextField()
    feedback_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-feedback_date',)
        
    def __str__(self):
        return self.property.title + "\t" + str(self.feedback_date)