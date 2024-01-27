from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.userlogin, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.userlogout, name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    path('profile/', views.userprofile, name='profile'),
    path('update-profile/', views.updateprofile, name='update_profile'),
    path('add-profile-picture/', views.add_profile_picture, name='add_profile_picture'),
    path('change-profile-picture/', views.change_profile_picture, name='change_profile_picture'),
    path('user/<username>', views.other_user, name='other_user'),
    path('follow/<username>', views.follow, name='follow'),
    path('unfollow/<username>', views.unfollow, name='unfollow'),
    path('search_user/', views.search_user, name='search_user')
]