
from django.contrib import admin
from . import views
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'pages'

urlpatterns = [
    
    path('<slug:pageslug>/', views.showpage, name="showpage" ),
    
]

# ref/templates/builtins.html#ref-templates-builtins-tags