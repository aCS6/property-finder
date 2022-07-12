from django.db import models

# Create your models here.


class ContactUS(models.Model):
    description = models.TextField(null=True,blank=True)
    map = models.ImageField(null=True,blank=True)
    email1 = models.EmailField(null=True,blank=True)
    email2 = models.EmailField(null=True,blank=True)
    phone1 = models.CharField(max_length=15,null=True,blank=True)
    phone2 = models.CharField(max_length=15,null=True,blank=True)
    address = models.CharField(max_length=350)
    facebook = models.URLField(max_length=350,null=True,blank=True)
    twitter = models.URLField(max_length=350,null=True,blank=True)
    youtube = models.URLField(max_length=350,null=True,blank=True)
    whatsapp = models.CharField(max_length=350,null=True,blank=True)


class Testimonial(models.Model):
    name = models.CharField(max_length=250,null=True,blank=True)
    image  = models.ImageField(upload_to="mainsite/testimonial")
    description = models.TextField()

    def __str__(self) -> str:
        return self.name

class AboutUs(models.Model):
    title = models.CharField(max_length=350,null=True,blank=True)
    slogan = models.CharField(max_length=350,null=True,blank=True)
    established_date = models.DateField(max_length=350,null=True,blank=True)
    description = models.TextField()
    privacy_policy = models.TextField()
    legal = models.TextField()
    mission = models.TextField()
    vision = models.TextField()

class OurServices(models.Model):
    service_title = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="mainsite/service")
    description = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.name
    