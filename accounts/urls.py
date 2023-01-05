
from django.conf.urls import url
from . import views
from django.urls import path

app_name = "accounts"

urlpatterns = [
    
    path('auth/signup/',views.signup_view, name="signup"),
    path('auth/login/',views.login_view, name="login"),
    path('auth/logout/',views.logout_view, name="logout"),
    
    
    path('profile/',views.profile, name="user-home"),
    path('profile/edit',views.profileEdit, name="user-edit"),
    path('profile/delete',views.profileDelete, name="user-delete"),
    path('profile/mycomments/',views.mycomments, name="user-comments"),
    path('profile/playlist/',views.playlist, name="user-playlist"),
    path('profile/favorites/',views.favorites, name="user-favorites"),
    

]

