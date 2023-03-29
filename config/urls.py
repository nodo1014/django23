from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('blog/', include('blog.urls')),
    path('', include('single_pages.urls')),
    path('admin/', admin.site.urls),
]
