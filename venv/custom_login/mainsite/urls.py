from django.urls import path
from mainsite import views

app_name = 'mainsite'
urlpatterns = [
    path('',views.index,name='index'),
    path('all/',views.all_property,name='all_property'),
    path('<int:pk>/',views.single_property,name="single_property"),
    path('profile/<int:pk>/',views.agent_single,name="agent_single"),
    path('properties/<str:status>/',views.navbar,name="status"),
    path('properties/<str:status>/<str:type>/',views.navbar_navigation,name="navbar"),
    path('search/',views.search,name="search"),
    path('about/',views.about,name="about")
] 