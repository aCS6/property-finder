from django import forms
import datetime
from django.forms.widgets import SelectDateWidget
from django.db.models import fields
from properties.models import Property


class dateInput(forms.DateInput):
    input_type = 'date'

class PropertyAddForm(forms.ModelForm):
    established_date = forms.DateField(widget=dateInput)
    class Meta:
        model = Property
        fields = [
            'title',
            'address',
            'city',
            'usage',
            'property_type',
            'status',
            'area',
            'area_unit',
            'description',
            'price',
            'bedroom',
            'bathroom',
            'garage',
            'kitchen',
            'image1',
            'image2',
            'amenities',
            'video_link',
            'map',
            'floor_plan',
            'established_date',
            'publish_price'
        ]