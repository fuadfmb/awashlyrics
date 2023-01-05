
from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'music'

urlpatterns = [
    
    # unauthorized urls
    path('admin/',views.error3 , name="admin"),
    path('media/',views.error3 , name="media"),
    path('media/<slug:slug>/',views.error3 , name="media-slug"),


    # auth = False
    path('', views.index, name="artist-home" ),
    path('artists/', views.all_artists, name="all_artists" ), 
    path('albums/', views.all_albums, name="all_albums" ),
    path('songs/', views.all_songs, name="all_songs" ),
    
    path('search/', views.search, name="search"),
    
    path('category/', views.category, name="category" ),
    path('category/<slug:category>/', views.showcategory, name="category_slug" ),
    
    path('gallery/', views.gallery, name="gallery" ),
    path('gallery/<slug:artist>/', views.artist_gallery, name="gallery_slug" ),
    
    path('<slug:artist>/', views.artist_artist, name="artist_page" ),
    path('<slug:artist>/<slug:album>/', views.artist_album, name="album_page" ),
    path('<slug:artist>/<slug:album>/<slug:song>/', views.artist_album_song, name="song_page" ),
    path('<slug:artist>/<slug:album>/<slug:song>/lyrics/', views.artist_album_song_lyrics, name="lyrics_page" ),
    
    
    # lyrics !!!
    
]


