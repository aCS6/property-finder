from django.contrib import admin
from properties import models

# Register your models here.
admin.site.register(models.City)
admin.site.register(models.Status)
admin.site.register(models.Usage)
admin.site.register(models.Property_type)
admin.site.register(models.Area_unit)
admin.site.register(models.Property)
admin.site.register(models.Feedback)