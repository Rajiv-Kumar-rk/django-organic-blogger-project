from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView, TemplateView
from App_Blog.models import Blog, Comment, Like
from App_Authentication.models import Follow
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import uuid
from App_Blog.forms import CommentForm
from django.contrib.auth.models import User
from App_Authentication.models import UserProfileModel
from django.urls import reverse, reverse_lazy

def home(request):
    blogs = Blog.objects.all().order_by('-publish_date')
    data = {
     'blogs' : blogs,    
    }
    return render(request, 'App_Blog/index.html', context=data)

class MyBlogs(LoginRequiredMixin, TemplateView):
    template_name = 'App_Blog/myBlogs.html'

class CreateBlog(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'App_Blog/createBlog.html'
    fields = ['title', 'content', 'image']
    blog_created = False

    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        title = blog_obj.title
        blog_obj.slug = title.replace(" ", "-") + "-" + str(uuid.uuid4())
        blog_obj.save()
        blog_created = True
        
        data={
            'blog_created' : blog_created
        }
        return render(self.request, 'App_Blog/createBlog.html', context=data)

@login_required
def delete_blog(request, pk):
    Blog.objects.get(pk=pk).delete()
    return redirect('profile')
    

class EditBlog(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ['title', 'content', 'image']
    template_name = 'App_Blog/editBlog.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('blog_details', kwargs={'slug':self.object.slug})


def blog_details(request, slug):
    if request.user.is_authenticated:
        blog_obj = Blog.objects.get(slug=slug)
        comment_form = CommentForm()
        blog_already_liked = Like.objects.filter(blog=blog_obj, user=request.user)
        is_blog_liked = False
        if blog_already_liked:
            is_blog_liked = True

        if request.method == 'POST':    
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.blog = blog_obj
                comment.save()
    
        data = {
            'blog' : blog_obj,
            'comment_form' : comment_form,
            'is_blog_liked' : is_blog_liked
        }
        #print('Name: '+ blog_obj.title)
        #print('Slug: '+ blog_obj.slug)
        return render(request, 'App_Blog/blogDetails.html', context=data)
    
    else:
        return redirect('login')

    

@login_required
def like_blog(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    blog_already_liked = Like.objects.filter(blog=blog, user=user)
    if not blog_already_liked: 
        blog_to_be_liked = Like(blog=blog, user=user)
        blog_to_be_liked.save()
        
        data = {
            'blog' : blog,
        }
        return redirect('blog_details', slug=blog.slug)

@login_required
def dislike_blog(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    blog_already_liked = Like.objects.filter(blog=blog, user=user)
    blog_already_liked.delete()

    data = {
        'blog' : blog
    }
    return redirect('blog_details', slug=blog.slug)