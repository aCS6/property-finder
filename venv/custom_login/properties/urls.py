from os import name
from django.urls import path
from properties import views 

app_name = 'properties'

urlpatterns = [
    path('',views.index,name='index'),
    path('add-properties/',views.add_properties,name='add_properties'),
    path('edit-properties/<int:pk>',views.edit_properties,name='edit_properties'),
    path('delete-properties/<int:pk>',views.delete_properties,name='delete_properties'),
    path('feedback/<int:pk>',views.feedback,name="feedback"),
    path('feedbacks',views.feedbacks,name="feedbacks")
]
