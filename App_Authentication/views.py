from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from App_Authentication.forms import UserRegistrationForm, UpadteUserDetailsForm, UserProfilePicture, UpdateUserProfileOtherInfo
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from App_Authentication.models import UserProfileModel, Follow
from App_Blog.models import Blog, Like, Comment
# Create your views here.

def register(request): 
    if request.user.is_authenticated: 
        return redirect('home')
    else:
        form = UserRegistrationForm()
        register_status = False
        if request.method == 'POST':
            form = UserRegistrationForm(data=request.POST)
            if form.is_valid():
                form.save()
                user = User.objects.get(username=request.POST.get('username'))
            
                userProfileOtherInfo = UserProfileModel(user=user)
                userProfileOtherInfo.save()
                register_status = True
    
        data = { 
            'register_status' : register_status,
            'register_form' : form,
        }
        return render(request, 'App_Authentication/register.html', context=data)
    

def userlogin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:    
        form = AuthenticationForm()

        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user) 
                    #print(username)
                    return redirect('home')

        data = {
        'login_form' : form
        }
        return render(request, 'App_Authentication/login.html', context=data)
    
@login_required
def userlogout(request):
    logout(request)
    return redirect('login')

def change_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        password_changed = False
        form = PasswordChangeForm(current_user)
        if request.method == 'POST':
            form = PasswordChangeForm(current_user, data=request.POST)
            if form.is_valid():
                form.save()
                password_changed = True
            
        data={
            'form' : form,
            'password_changed' : password_changed
        }
        return render(request, 'App_Authentication/changePassword.html', context=data)
    else:
        return redirect('login')

def userprofile(request):
    if request.user.is_authenticated:
        blogs = Blog.objects.filter(author=request.user).order_by('-publish_date')
        data = {
            'blogs' : blogs
        }
        return render(request, 'App_Authentication/profile.html', context=data)
    else:
        return redirect('login')


def updateprofile(request):
    if request.user.is_authenticated:
        current_user = request.user
        profile_updated =False
        form1 = UpadteUserDetailsForm(instance=current_user)
        form2 = UpdateUserProfileOtherInfo(instance=UserProfileModel.objects.get(user=request.user))
        if request.method == 'POST':
            form1 = UpadteUserDetailsForm(data=request.POST, instance=current_user)
            form2 = UpdateUserProfileOtherInfo(data=request.POST, instance=UserProfileModel.objects.get(user=request.user))
            if form1.is_valid()  and form2.is_valid():
                form1.save()
                form2.save()
                form1 = UpadteUserDetailsForm(instance=current_user)
                form2 = UpdateUserProfileOtherInfo(instance=UserProfileModel.objects.get(user=request.user))
            
                profile_updated = True
    
        data = {
            'form1' : form1,
            'form2' : form2, 
            'profile_updated' : profile_updated
        }
        return render(request, 'App_Authentication/updateProfile.html', context=data) 
    else:
        return redirect('login')


def add_profile_picture(request):
    if request.user.is_authenticated:
        profile_pic_added = False
        form = UserProfilePicture() 
        if request.method == 'POST':
            form = UserProfilePicture(request.POST, request.FILES)
            if form.is_valid():
                user_pic = form.cleaned_data.get('profile_pic')
                user_obj = UserProfileModel.objects.get(user=request.user)
                user_obj.profile_pic = user_pic
                user_obj.save()
                profile_pic_added = True
            
        data = {
            'form' : form,
            'profile_pic_added' : profile_pic_added
        }
        return render(request, 'App_Authentication/addUserProfilePicture.html', context=data)
    else:
        return redirect('login')


def change_profile_picture(request):
    if request.user.is_authenticated:
        current_user = request.user
        profile_pic_updated = False
        form = UserProfilePicture(instance=current_user.user_profile)
        if request.method == 'POST':
            form = UserProfilePicture(request.POST, request.FILES, instance=current_user.user_profile)
            if form.is_valid():
                form.save()
                profile_pic_updated= True
            
        data = {
            'form' : form,
            'profile_pic_updated' : profile_pic_updated
        }
        return render(request, 'App_Authentication/updateUserProfilePicture.html', context=data)
    else:
        return redirect('login')


def other_user(request, username):
    if request.user.is_authenticated:
        other_user_obj = User.objects.get(username=username)
        already_followed = Follow.objects.filter(follower=request.user, following=other_user_obj)
        blogs = Blog.objects.filter(author=other_user_obj).order_by('-publish_date')
        if other_user_obj == request.user:
            return redirect('profile')

        data = {
            'other_user_profile' : other_user_obj,
            'is_already_followed' : already_followed,
            'blogs' : blogs
        }
        return render(request, 'App_Authentication/otherUserProfile.html', context=data)
    else:
        return redirect('login')

@login_required
def follow(request, username):
    follower = request.user
    following_to_user = User.objects.get(username=username)
    already_followed = Follow.objects.filter(follower=follower, following=following_to_user)
    if not already_followed:
        followed_user_obj = Follow(follower=follower, following=following_to_user)
        followed_user_obj.save()
    
        return redirect('other_user', username=username)


@login_required
def unfollow(request, username):
    follower = request.user
    following_to_user = User.objects.get(username=username)
    already_followed = Follow.objects.filter(follower=follower, following=following_to_user)
    already_followed.delete()
    
    return redirect('other_user', username=username)


def search_user(request):
    if request.user.is_authenticated and request.method == 'GET':
        searched_item = request.GET.get('searched_user','')
        search_result = User.objects.filter(username__icontains=searched_item)
        empty_search = False
        if len(str(searched_item))==0:
            empty_search = True
        data = {
            'searched_item' : searched_item,
            'search_result' : search_result,
            'empty_search' : empty_search
        }
        return render(request, 'App_Authentication/searchUser.html', context=data)
