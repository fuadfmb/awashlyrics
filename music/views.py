from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound, Http404
from . models import *
from django.template import loader
from django.urls import reverse
from datetime import datetime
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.http import JsonResponse

def index(request, msgs = {} ):
    
    all_artists = Artist.objects.order_by('art_username')[:12]
    all_albums = Album.objects.order_by('alb_title' ).exclude(  alb_title = 'singles' )[:12]
    categories = Category.objects.all()

    # trending albums : add album views and increment every time user clicks... 
    trending_albums = Album.objects.order_by(
            '-alb_views'
        ).exclude( 
            alb_title = 'singles' 
        ) [:6]
    trending_songs = Song.objects.order_by(
            '-song_views'
        ) [:5]
    
    template = loader.get_template('music/index.html')
    context = {
        'artists': all_artists,
        'albums': all_albums,
        'trending_albums': trending_albums,
        'categories': categories,
        'trending_songs':trending_songs,
    }
    for key,value in msgs: context[key] = value
    
    return HttpResponse( template.render(context, request) )

# /artist/
def artist_artist(request, artist):
    artist = get_object_or_404(Artist, art_username=artist)
    albums = Album.objects.filter(artist=artist.id)
    # select * from songs where song.album.artist.id = artist.id
    m_songs = Song.objects.filter( album__artist__id=artist.id )
    categories = Category.objects.all()
    
    # paginate songs
    paginator = Paginator(m_songs, 10)
    page_number = request.GET.get('page')
    songs = paginator.get_page(page_number)
    
    template = loader.get_template('music/art_home.html')
    context = {
        'artist': artist,
        'albums': albums,
        'songs': songs,
        'm_songs': m_songs.count(),
        'categories':categories,
    }
    return HttpResponse( template.render(context, request) )

# /artist/album/
def artist_album(request, artist, album):
    message = ""
    messageType = ""
    userInput = ""
    
    artist = get_object_or_404(Artist, art_username=artist)
    album = get_object_or_404(Album, alb_slug=album, artist_id=artist.id )
    albums = Album.objects.filter(artist=artist.id)
    categories = Category.objects.order_by('cat_name')
    mSongs = album.song_set.all()
    comments = album.albumcomments_set.filter(
        approved = True,
        deleted = False
        )[:20]
    
    if request.method == "POST":
        if request.user.is_authenticated:
            # print( request.POST )
            if request.POST.get('comment'):
                if len(request.POST.get('comment')) < 10:
                    messageType = "error"
                    message = 'A comment should have to be at least 10 characters long!'
                    userInput = request.POST.get('comment').strip()
                elif len(request.POST.get('comment')) > 500:
                    messageType = "error"
                    message = "That's too much! minimize your comment down to 500 characters !"
                    userInput = request.POST.get('comment').strip()
                else:
                    # if there is 'edit' in the request, it's edit comment
                    if request.POST.get('edit'):
                        oldComment = get_object_or_404(AlbumComments, id=request.POST.get('edit') )
                        if oldComment.commented_user.id == request.user.id and album.id == oldComment.commented_on_album.id and oldComment.deleted == False:
                            oldComment.comment = request.POST.get('comment')
                            oldComment.save()
                            messageType = "success"
                            message = "Comment updated successfully !"
                        else:
                            messageType = "error"
                            message = 'Something went wrong! That\'s all we know!'
                    else:
                        # else it's a new comment
                        newComment = AlbumComments()
                        newComment.commented_on_date  = datetime.now()
                        newComment.commented_on_album = album
                        newComment.commented_user  = request.user
                        newComment.comment = request.POST.get('comment')
                        newComment.approved = True
                        newComment.save()
                        messageType = "success"
                        message = "Comment added successfully !"
            elif request.POST.get('delete'):
                comment_id = request.POST.get('delete')
                comment = get_object_or_404(AlbumComments, id=comment_id)
                if request.user.id == comment.commented_user.id and album.id == comment.commented_on_album.id and comment.approved == True:
                    comment.deleted = True
                    comment.save()
                    
                    messageType = "success"
                    message = "Comment deleted successfully!"
                else:
                    messageType = "error"
                    message = "Something went wrong. That\'s all we know!"
                print( request.POST.get('delete') )
        else:
            messageType = "error"
            message = "You need to login first !"
    
    paginator = Paginator(mSongs, 10)
    page_number = request.GET.get('page')
    songs = paginator.get_page(page_number)
    
    # increment alb_views
    from django.db.models import F
    album.alb_views = F('alb_views') + 1
    album.save()
    
    template = loader.get_template('music/art_album.html')
    context = {
        'artist': artist,
        'album': album,
        'albums':albums,
        'songs':songs,
        'categories':categories,
        'comments':comments,
        'message':message,
        'messageType':messageType,
        'userInput': userInput,
    }
    return HttpResponse( template.render(context, request) )

# /artist/album/song/
def artist_album_song(request, artist, album, song):
    message = ""
    messageType = ""
    userInput = ""
    
    artist = get_object_or_404(Artist, art_username=artist)
    album = get_object_or_404(Album, alb_slug=album, artist_id=artist.id )
    song = get_object_or_404(Song, song_slug=song)
    lyrics = song.lyrics_set.all()
    # print( lyrics.count() )
    has_lyrics = True if lyrics.count() else False
    # print( has_lyrics )
    comments = song.songcomments_set.filter(
        approved = True,
        deleted = False
        )[:20]
    favorited = SongLikes.objects.filter(liked_user__id=request.user.id, liked_song__id=song.id)
    playlisted = Playlist.objects.filter(user__id=request.user.id, song__id=song.id)
    
    # increment song_views
    from django.db.models import F
    song.song_views = F('song_views') + 1
    song.save()
    
    if request.method == "POST":
        if request.user.is_authenticated:
            # comment
            if request.POST.get('comment'):
                if len(request.POST.get('comment')) < 10:
                    messageType = "error"
                    message = 'A comment should have to be at least 10 characters long!'
                    userInput = request.POST.get('comment').strip()
                elif len(request.POST.get('comment')) > 500:
                    messageType = "error"
                    message = "That's too much! minimize your comment down to 500 characters !"
                    userInput = request.POST.get('comment').strip()
                else:
                    if request.POST.get('edit'):
                        oldComment = get_object_or_404(SongComments, id=request.POST.get('edit') )
                        if oldComment.commented_user.id == request.user.id and song.id == oldComment.commented_on_song.id and oldComment.deleted == False:
                            oldComment.comment = request.POST.get('comment')
                            oldComment.save()
                            messageType = "success"
                            message = "Comment updated successfully !"
                        else:
                            messageType = "error"
                            message = 'Something went wrong! That\'s all we know!'
                    else:
                        newComment = SongComments()
                        newComment.commented_date = datetime.now()
                        newComment.commented_on_song = song
                        newComment.commented_user = request.user
                        newComment.comment = request.POST.get('comment')
                        newComment.approved = True
                        newComment.save()
                        messageType = "success"
                        message = "Comment added successfully!"
            # Like
            elif request.POST.get('like'):
                if ( len(favorited) > 0 ): # already liked !
                    favorited.delete()
                    return HttpResponse( 'unliked')
                else:
                    mlike = SongLikes( liked_date = datetime.now(), liked_user = request.user, liked_song = song )
                    mlike.save()
                    return HttpResponse('liked')
            # playlist
            elif request.POST.get('playlist'):
                if ( len(playlisted) > 0 ): # already added to playlist !
                    print('removed')
                    playlisted.delete()
                    return HttpResponse( 'removed')
                
                else:
                    mplaylist = Playlist( added_date = datetime.now(), user = request.user, song = song )
                    mplaylist.save()
                    print('added')
                    return HttpResponse('added')
                print('here...')
            
            # delete
            elif request.POST.get('delete'):
                comment_id = request.POST.get('delete')
                comment = get_object_or_404(SongComments, id=comment_id)
                if request.user.id == comment.commented_user.id and song.id == comment.commented_on_song.id and comment.approved == True:
                    comment.deleted = True
                    comment.save()
                    # comment.delete() we don't do that ;)
                    messageType = "success"
                    message = "Comment deleted successfully!"
                else:
                    messageType = "error"
                    message = "Something went wrong. That's all we know!"
                print( request.POST.get('delete') )
        else:
            messageType = "error"
            message = "You need to login first !"
    
    template = loader.get_template('music/art_song.html')
    context = {
        'artist': artist,
        'album': album,
        'song': song,
        'comments': comments,
        'message': message,
        'messageType': messageType,
        'userInput':  userInput,
        'favorited': favorited,
        'playlisted': playlisted,
        'has_lyrics': has_lyrics,
    }
    return HttpResponse( template.render(context, request) )

# /artist/album/song/lyrics/
def artist_album_song_lyrics(request, artist, album, song):

    artist = get_object_or_404(Artist, art_username=artist)
    album = get_object_or_404(Album, alb_slug=album, artist_id=artist.id )
    song = get_object_or_404(Song, song_slug=song)
    lyrics = song.lyrics_set.all()
    comments = song.songcomments_set.filter(
        approved = True,
        deleted = False
        )[:20]

    # increment song_views
    from django.db.models import F
    song.song_views = F('song_views') + 1
    song.save()
    
    template = loader.get_template('music/art_lyrics.html')
    context = {
        'artist': artist,
        'album': album,
        'song': song,
        'comments': comments,
        'lyrics':lyrics,
    }
    return HttpResponse( template.render(context, request) )




def artist_gallery(request, artist):
    artist = get_object_or_404(Artist, art_username=artist)
    photos = ArtImage.objects.filter( gallery__artist__id = artist.id ) 
    
    categories = Category.objects.all()
    template = loader.get_template('music/art_gallery.html')
    trending_albums = Album.objects.order_by(
            '-alb_views'
        ).exclude( 
            alb_title = 'singles' 
        ) [:6]
    
    context = {
        'artist':artist,
        'photos': photos,
        'trending_albums':trending_albums,
        'categories':categories,
    }
    return HttpResponse( template.render(context, request) )

def search(request):
    from django.db.models import Q
    table = request.GET.get('in')
    query = request.GET.get('q')
    
    categories = Category.objects.all()
    template = loader.get_template('music/search.html')
    trending_albums = Album.objects.order_by(
            'alb_release_date'
        ).exclude( 
            alb_title = 'singles' 
        ) [:6]
    
    if request.method == "GET":
        if query == "" or table == "" or not table in ['artists','albums','songs'] :
            return redirect('music:artist-home')
        else:
            context = {
                    'trending_albums':trending_albums,
                    'categories':categories,
                    'query':query,
                    'table':table
            }
            if table == "artists":
                artists = Artist.objects.filter(
                    Q(art_firstname__icontains=query) | Q(art_lastname__icontains=query) | Q(art_username__icontains=query) |
                    Q(art_meta_tags__icontains=query) | Q(art_about__icontains=query)
                )
                paginator = Paginator(artists, 10)
                page_number = request.GET.get('page')
                artists = paginator.get_page(page_number)
                
                context['artists']=artists
                
            elif table == "albums":
                albums = Album.objects.filter(
                    Q(alb_title__icontains=query) | Q(alb_slug__icontains=query) | Q(alb_about__icontains=query) |
                    Q(alb_meta_tags__icontains=query)
                    
                )
                paginator = Paginator(albums, 10)
                page_number = request.GET.get('page')
                albums = paginator.get_page(page_number)
                
                context['albums']=albums
            
            elif table == "songs":
                songs = Song.objects.filter(
                    Q(song_title__icontains=query) | Q(song_slug__icontains=query) | Q(song_meta_tags__icontains=query)
                )
                paginator = Paginator(songs, 10)
                page_number = request.GET.get('page')
                songs = paginator.get_page(page_number)
                
                context['songs']=songs
            
            # render
            return HttpResponse( template.render(context, request) )
    else:
        return HttpResponse('<h2 style="margin: 20px;">Gah ! page not found :( <br><br> <a href="/">Home</a></h2>')
    
def error1(request):
    template = loader.get_template('music/error.html')
    context = {
        'error': "Page Not Found :(",
    }
    return HttpResponse( template.render(context, request) )

def error2(request):
    template = loader.get_template('music/error.html')
    context = {
        'error': "Fill the form correctly :(",
    }
    return HttpResponse( template.render(context, request) )
    return HttpResponse( template.render(context, request) )

def error3(request, slug='-'):
    template = loader.get_template('music/error.html')
    context = {
        'error': "You are not allowed here :(",
    }
    return HttpResponse( template.render(context, request) )
    
################################
# all_artists, all_albums, all_songs, ...
################################

def all_artists(request):
    all_artists = Artist.objects.order_by('art_username')
    categories = Category.objects.all()

    # paginate artists
    paginator = Paginator(all_artists, 12)
    page_number = request.GET.get('art')
    artists = paginator.get_page(page_number)

    # trending albums : add album views and increment every time user clicks... 
    trending_albums = Album.objects.order_by(
            'alb_release_date'
        ).exclude( 
            alb_title = 'singles' 
        ) [:6]
    template = loader.get_template('music/all_artists.html')
    context = {
        'artists': artists,
        'trending_albums': trending_albums,
        'categories':categories,
    }
    return HttpResponse( template.render(context, request) )

def all_albums(request):
    all_albums = Album.objects.order_by('alb_title' ).exclude(  alb_title = 'singles' )
    categories = Category.objects.all()
    
    # paginate albums
    paginator = Paginator(all_albums, 12)
    page_number = request.GET.get('alb')
    albums = paginator.get_page(page_number)
    
    # trending albums : add album views and increment every time user clicks... 
    trending_albums = Album.objects.order_by(
            'alb_release_date'
        ).exclude( 
            alb_title = 'singles' 
        ) [:6]
    template = loader.get_template('music/all_albums.html')
    context = {
        'albums': albums,
        'trending_albums': trending_albums,
        'categories':categories,
    }
    return HttpResponse( template.render(context, request) )

def all_songs(request):
    all_songs = Song.objects.order_by('song_title' )
    categories = Category.objects.all()

    # paginate songs
    paginator = Paginator(all_songs, 10)
    page_number = request.GET.get('song')
    songs = paginator.get_page(page_number)
     
    trending_albums = Album.objects.order_by(
            '-alb_views'
        ).exclude( 
            alb_title = 'singles' 
        ) [:6]
    template = loader.get_template('music/all_songs.html')
    context = {
        'songs': songs,
        'trending_albums': trending_albums,
        'categories':categories,
    }
    return HttpResponse( template.render(context, request) )

def category(request):
    category = Category.objects.all()
    
    paginator = Paginator(category, 8)
    page_number = request.GET.get('page')
    categories = paginator.get_page(page_number)
    
    template = loader.get_template('music/category.html')
    trending_albums = Album.objects.order_by(
            '-alb_views'
        ).exclude( 
            alb_title = 'singles' 
        ) [:6]
    context = {
        'categories': categories,
        'mcategories': category,
        'trending_albums': trending_albums,
    }
    return HttpResponse( template.render(context, request) )

def gallery(request):
    gallery = Gallery.objects.all()
    categories = Category.objects.all()
    
    paginator = Paginator(gallery, 8)
    page_number = request.GET.get('page')
    galleries = paginator.get_page(page_number)
    
    template = loader.get_template('music/gallery.html')
    trending_albums = Album.objects.order_by(
            '-alb_views'
        ).exclude( 
            alb_title = 'singles' 
        ) [:6]
    context = {
        'galleries': galleries,
        'categories': categories,
        'trending_albums': trending_albums,
    }
    return HttpResponse( template.render(context, request) )

def showcategory(request, category):
    mcategory = get_object_or_404(Category, cat_slug=category)
    cat_music = mcategory.song_set.all()
    categories = Category.objects.all()

    paginator = Paginator(cat_music, 10)
    page_number = request.GET.get('song')
    songs = paginator.get_page(page_number)
     
    trending_albums = Album.objects.order_by(
            '-alb_views'
        ).exclude( 
            alb_title = 'singles' 
        ) [:6]
    template = loader.get_template('music/cat_music.html')
    context = {
        'songs': songs,
        'trending_albums': trending_albums,
        'categories': categories,
        'category': mcategory,
    }
    return HttpResponse( template.render(context, request) )







