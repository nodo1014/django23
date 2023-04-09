from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('blog/', include('blog.urls')),
    path('', include('single_pages.urls')),
    path('admin/', admin.site.urls),
    path('markdownx/', include('markdownx.urls')),
]

# static() 정적 파일들의 url을 관리. 접근한 url을 리턴.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)