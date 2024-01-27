from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from App_Authentication.models import UserProfileModel

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email Address', required=True)

    #email = forms.EmailField(required=True, label="", widget=forms.TextInput(attrs={'placeholder':'Your Email'}))
    #password = forms.CharField(required=True, label="", widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        

class UpadteUserDetailsForm(forms.ModelForm):
    first_name = forms.CharField(label='First name', required=True)
    last_name = forms.CharField(label='Last name', required=True)
    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'first_name',  
            'last_name'
        ]

class UpdateUserProfileOtherInfo(forms.ModelForm):
    class Meta:
        model = UserProfileModel
        fields = [
            'discription',
            'instagram_profile_link',
            'facebook_profile_link',
            'twitter_profile_link',
            'linkedin_profile_link'
        ]

class UserProfilePicture(forms.ModelForm):
    class Meta:
        model = UserProfileModel
        fields = ['profile_pic']

