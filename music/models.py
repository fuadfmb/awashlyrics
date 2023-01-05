from django.db import models
from django.utils import timezone
from datetime import datetime
import time
from django.core.validators import FileExtensionValidator
from django.views.generic import ListView
from django.contrib.auth.models import User

def music_directory_path(instance, filename):
    return 'songs/song_{0}_{1}'.format( time.time() , filename)

def image_directory_path(instance, filename):
    return 'gallery/img_{0}_{1}'.format( time.time() , filename)

class Language(models.Model):
    lang_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.lang_name
    
    def lyrics_Count(self):
        return len( self.lyrics_set.all() )

class Category(models.Model):
    cat_name = models.CharField(max_length=50)
    cat_slug = models.CharField(max_length=50, unique=True )
    cat_cover_pic = models.FileField(upload_to=image_directory_path, 
        validators=[FileExtensionValidator(
                        ['jpg','png','gif']
                    )]
    )
    
    def __str__(self):
        return self.cat_name
    
    def songs_Count(self):
        return len(self.song_set.all() )
    
    class Meta:
        verbose_name_plural = "Categories"

class Artist(models.Model):
    art_firstname = models.CharField(max_length=50)
    art_lastname = models.CharField(max_length=50)
    art_username = models.CharField(max_length=50, unique=True)
    art_about = models.TextField(max_length=1000, blank=True)
    art_meta_tags = models.TextField(max_length=1000, blank=True, default="-")
    added_date = models.DateTimeField( blank=True, null=True )
    art_prof_pic = models.FileField(upload_to=image_directory_path, 
        validators=[FileExtensionValidator(
                        ['jpg','png','gif']
                    )]
    )

    def __str__(self):
        return self.art_username
    
    def albums(self):
        return len( self.album_set.all() )
    
    class Meta:
        ordering = ['art_username']
        verbose_name_plural = "    Artists"
    
    @property
    def full_name(self):
        return '%s %s' % (self.art_firstname, self.art_lastname)
    
    # create singles Album for this artist just after save()
    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)
        
        # create 'singles' album for this artist !
        
        albumtitle = "singles"
        albumabout = self.art_username + " singles collection"
        alb_slug = "singles"
        alb_rel_date = str( datetime.now() )
        cover = "gallery/singles.png"
        artist = str( self.id )
        
        from django.db import connection
        with connection.cursor() as cursor:
            query = "insert into music_album(\
                'alb_title','alb_slug','alb_about','alb_release_date','alb_views', 'alb_meta_tags','alb_cover', 'artist_id'\
                    ) values('%s','%s','%s','%s','%s','%s', '%s', '%s')" % ( 
                albumtitle, alb_slug, albumabout, alb_rel_date, '1', '-', cover, artist
                )
            # 
            check = "select * from music_album where artist_id='" + str(self.id) + "' AND alb_title='singles'"
            c = cursor.execute(check)
            row = c.fetchone()
            if not row : # only if not available, create a new one !
                cursor.execute( query )
        # docs  /topics/db/sql.html
        
class Album(models.Model):
    alb_title = models.CharField(max_length=50)
    alb_slug = models.CharField(max_length=50)
    alb_about = models.CharField(max_length=1000, blank=True, null=True)
    alb_release_date = models.DateTimeField( auto_now=True, blank=True, null=True )
    alb_views = models.BigIntegerField(default=1)
    alb_meta_tags = models.TextField(max_length=1000, blank=True, default="-")
    alb_cover = models.FileField(upload_to=image_directory_path, 
        validators=[FileExtensionValidator(
                        ['jpg','png','gif']
                    )]
    )

    # an album belongs to an artist
    artist = models.ForeignKey(
        Artist, 
        on_delete=models.CASCADE
    )
    def songs_count(self):
        return len( self.song_set.all() )
    def __str__(self):
        return self.artist.art_username + " - " + self.alb_title
    
    class Meta:
        ordering = ['alb_title']
        verbose_name_plural = "   Albums"

class Song(models.Model):
    song_title = models.CharField(max_length=50)
    song_slug = models.CharField(max_length=50, unique=True)
    song_views = models.BigIntegerField(default=1)
    added_date = models.DateTimeField( auto_now=True, blank=True, null=True)
    song_meta_tags = models.TextField(max_length=1000, blank=True, default="-")
    song_category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        default='Uncategorized'
    )
    song_yt_link = models.CharField(max_length=50, blank=True)
    song_file = models.FileField(upload_to=music_directory_path, 
        validators=[FileExtensionValidator(
                        ['mp3','ogg','aac']
                    )]
    )
    
    # a song belongs to an album
    album = models.ForeignKey(
        Album, 
        on_delete=models.CASCADE
    )
    def __str__(self):
        # return self.album.artist.name + " - " + self.album.title + " - " + self.title
        return f'{self.album.artist.art_username}- {self.album.alb_title} - {self.song_title}'

    def has_Lyrics(self):
        x = self.lyrics_set.all()
        return True if len(x) > 0 else False

    has_Lyrics.boolean = True
    has_Lyrics.short_description = "Has Lyrics?"

    class Meta:
        ordering = ['song_title']
        verbose_name_plural = "  Songs"

class Lyrics(models.Model):
    ly_full = models.TextField()
    
    # lyrics can be translated
    ly_lang = models.ForeignKey(
        Language, 
        on_delete=models.CASCADE
    )
    # lyrics belongs to a song
    ly_song = models.ForeignKey(
        Song, 
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        # return self.album.artist.name + " - " + self.album.title + " - " + self.title
        return self.ly_song.album.artist.art_username + " - " + self.ly_song.song_title
    
    class Meta:
        verbose_name_plural = " Lyrics"

class Gallery(models.Model):
    # an artist can have it's own photo gallery
    artist = models.ForeignKey(
        Artist, 
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return self.artist.art_username + "'s Gallery"
    
    class Meta:
        verbose_name_plural = "Galleries"
        
    def photos(self):
        return len( self.artimage_set.all() )
    
class ArtImage(models.Model):
    gallery = models.ForeignKey(
        Gallery, 
        on_delete=models.CASCADE
    )
    image_file = models.FileField(upload_to=image_directory_path, 
        validators=[FileExtensionValidator(
                        ['jpg','png','gif']
                    )]
    )
    def __str__(self):
        return self.gallery.artist.art_username + "'s Image "+ str(self.id)

class AlbumComments(models.Model):
    comment = models.TextField(default='-', max_length=500)
    commented_on_date = models.DateTimeField()
    commented_on_album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE
    )
    commented_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    approved = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.comment

    class Meta:
        verbose_name_plural = "Album Comments"
        
    def snippet(self):
        if len(self.comment) <= 50:
            return self.comment
        return self.comment[:50] + '...'

    def short_comment(self):
        if len(self.comment) <= 150:
            return self.comment
        return self.comment[:150] + '...'
    
    def isapproved(self):
        return True if self.approved else False
    
    isapproved.boolean = True
    isapproved.short_description = "Approved?"

class SongComments(models.Model):
    comment = models.TextField(default='-', max_length=500)
    commented_date = models.DateTimeField(auto_now=True)
    commented_on_song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE
    )
    commented_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    approved = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name_plural = "Song Comments"
        
    def isapproved(self):
        return True if self.approved else False
    
    isapproved.boolean = True
    isapproved.short_description = "Approved?"
        
    def snippet(self):
        if len(self.comment) <= 50:
            return self.comment
        return self.comment[:50] + '...'

    def short_comment(self):
        if len(self.comment) <= 150:
            return self.comment
        return self.comment[:150] + '...'

class SongLikes(models.Model):
    liked_date = models.DateTimeField(auto_now=True)
    liked_song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE
    )
    liked_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return self.liked_user.username

    class Meta:
        verbose_name_plural = "Song Likes"

class Playlist(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE
    )
    added_date = models.DateTimeField(auto_now=True)



