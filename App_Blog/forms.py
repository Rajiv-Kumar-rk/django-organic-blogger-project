from django import forms
from App_Blog.models import Blog, Comment, Like

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
