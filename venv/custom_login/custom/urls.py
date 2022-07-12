from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

urlpatterns = [
    path('',include('mainsite.urls')),
    path('properties/',include('properties.urls')),
    path('pages/',include('pages.urls')),
    path('accounts/',include('accounts.urls')),
    path('blog/',include('blog.urls')),
    path('admin/', admin.site.urls),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)