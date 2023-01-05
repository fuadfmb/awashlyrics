from django.contrib import admin
from .models import *

class ArtistsList(admin.ModelAdmin):
    class AlbumInline(admin.StackedInline):
        model = Album
        extra = 0
    search_fields = [
        'art_username',
        'art_meta_tags',
        'art_firstname',
        'art_lastname',
        'art_about',
        ]
    list_display = ('art_username', 'albums', 'art_meta_tags', 'art_about' )
    list_filter = ['added_date']
    inlines = [ AlbumInline ]

class AlbumsList(admin.ModelAdmin):
    class SongInline(admin.StackedInline):
        model = Song
        extra = 0
    search_fields = [
        'alb_title',
        'alb_slug',
        'alb_about',
        'alb_meta_tags',
        ]
    list_display = ('__str__', 'alb_meta_tags', 'alb_about', 'songs_count')
    list_filter = ['alb_release_date']
    inlines = [ SongInline ]
    
class SongsList(admin.ModelAdmin):
    class LyricsInline(admin.StackedInline):
        model = Lyrics
        extra = 0
    search_fields = [
        'song_title',
        'song_slug',
        'song_meta_tags',
        ]
    list_display = ('song_slug', 'album', 'song_meta_tags', 'has_Lyrics')
    list_filter = ['added_date', 'song_category']
    inlines = [ LyricsInline ]

class ImagesInlines(admin.ModelAdmin):
    # class ImagesInline(admin.TabularInline):
    class ImagesInline(admin.StackedInline):
        model = ArtImage
        extra = 0
    inlines = [ImagesInline]
    list_display = ['__str__', 'photos']
 
class CategoryList(admin.ModelAdmin):
    class SongsInline(admin.StackedInline):
        model = Song
        extra = 0
    search_fields = [
        'cat_name',
        'cat_slug',
        ]
    list_display = ('cat_name', 'songs_Count')
    list_filter = ['cat_name', 'cat_slug']
    inlines = [ SongsInline ]

class LanguagesList(admin.ModelAdmin):
    search_fields = [
        'lang_name',
        ]
    list_display = ('lang_name', 'lyrics_Count')
    list_filter = ['lang_name']

class Comment4Album(admin.ModelAdmin):
    search_fields = [
        'comment',
        ]
    list_display = ( 'commented_on_album','commented_user','snippet','isapproved')
    list_filter = ['commented_on_date', 'approved']

class Comment4Song(admin.ModelAdmin):
    search_fields = [
        'comment',
        ]
    list_display = ( 'commented_on_song','commented_user','snippet','isapproved')
    list_filter = ['commented_date', 'approved']

class ShowSongLikes( admin.ModelAdmin ):
    search_fields = [
        'liked_song',
        ]
    list_display = ( 'liked_song','liked_user','liked_date' )
    list_filter = ['liked_date']
    
class ShowPlaylist( admin.ModelAdmin ):
    search_fields = [
        'song',
        ]
    list_display = ( 'song','user','added_date' )
    list_filter = ['added_date']


admin.site.register(Artist, ArtistsList)
admin.site.register(Album, AlbumsList)
admin.site.register(Song, SongsList)
admin.site.register(Lyrics)
admin.site.register(Playlist, ShowPlaylist)
admin.site.register(SongLikes, ShowSongLikes)
admin.site.register(Gallery, ImagesInlines)
admin.site.register(Language, LanguagesList)
admin.site.register(Category, CategoryList)
admin.site.register(AlbumComments, Comment4Album)
admin.site.register(SongComments, Comment4Song)


