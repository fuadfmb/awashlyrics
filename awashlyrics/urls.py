
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    
    path('o/k/admin/', admin.site.urls),
    path('favicon.ico', views.favicon),
    # path('auth/', include('accounts.urls')),
    path('page/', include('pages.urls')),
    
    path('', include('accounts.urls')),
    path('', include('music.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



