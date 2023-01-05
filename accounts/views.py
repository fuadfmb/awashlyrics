from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth import login,logout
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound, Http404
from . models import *
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import *
from django.core.validators import validate_email
from music.models import *

def check_email(string):
    try:
        validate_email( string )
        return True
    except:
        return False

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("music:artist-home")
    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('music:artist-home')
        else:
            form = UserCreationForm()
        return render(request, 'accounts/signup.html', {'form':form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("music:artist-home")
    else:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))    
                return redirect('music:artist-home')
        else:
            form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form':form})
    
def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("music:artist-home")

@login_required
def profile(request):
    
    user = get_object_or_404(User, username=request.user)
    
    template = loader.get_template('accounts/profile_home.html')
    context = {
        'user': user,
    }
    return HttpResponse( template.render(context, request) )

@login_required
def profileEdit(request):
    user = get_object_or_404(User, username=request.user)
    message = []
    messageType = ''
    if request.method == 'POST':
        print(request.POST)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        
        if 3<=len(first_name)<=30 and 3<=len(last_name)<=30 and check_email(string=email):
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            
            messageType = 'success'
            message.append('Profile updated successfully !')
        else:
            messageType = 'error'
            if not ( 3<=len(first_name)<=30 and 3<=len(last_name)<=30):
                message.append('Enter a valid name!')
            if not check_email(string=email):
                message.append('Enter a valid email address !')
        
    template = loader.get_template('accounts/profile_edit.html')
    context = {
        'user': user,
        'message':message,
        'messageType': messageType,
    }
    return HttpResponse( template.render(context, request) )

@login_required
def profileDelete(request):
    user = get_object_or_404(User, username=request.user)
    
    if request.method == "POST":
        logout(request)
        user.is_active = False
        user.save()
        msg = 'Account deleted successfully !'
        return redirect("music:artist-home")
    
    template = loader.get_template('accounts/profile_delete.html')
    context = {
        'user': user,
    }
    return HttpResponse( template.render(context, request) )

@login_required
def mycomments(request):
    return HttpResponse('profile')

@login_required
def playlist(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.POST.get('remove'):
                print( request.POST.get('remove') )
                # 
                mitem = get_object_or_404(Playlist, id=request.POST.get('remove'))
                if mitem.user == request.user :
                    mitem.delete()
                    return HttpResponse('removed')
                else:
                    return HttpResponse('error')
    
    playlists = Playlist.objects.filter(user__id=request.user.id)
    template = loader.get_template('accounts/playlist.html')
    context = {
        'playlists': playlists,
    }
    return HttpResponse( template.render(context, request) )

@login_required
def favorites(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.POST.get('remove'):
                print( request.POST.get('remove') )
                # 
                mitem = get_object_or_404(SongLikes, id=request.POST.get('remove'))
                if mitem.liked_user == request.user :
                    mitem.delete()
                    return HttpResponse('removed')
                else:
                    return HttpResponse('error')
    
    favorites = SongLikes.objects.filter(liked_user=request.user.id)
    template = loader.get_template('accounts/favorites.html')
    context = {
        'favorites': favorites,
    }
    return HttpResponse( template.render(context, request) )

