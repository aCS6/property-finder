from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogList.as_view(), name='blog_list'),
    path('write/', views.CreateBlog.as_view(), name='create_blog'),
    path('details/<slug:slug>', views.blog_details, name='blog_details'),
    path('my-blogs/', views.MyBlogs.as_view(), name='my_blogs'),
    path('edit/<pk>/', views.UpdateBlog.as_view(), name='edit_blog'),
    path('delete/<pk>/', views.DeleteBlog.as_view(), name='delete_blog'),
    path('individual-blog/<pk>/', views.Individual, name='individual'),
]
