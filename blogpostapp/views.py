from django.shortcuts import render
from .models import Post
from django.views.generic import (ListView, 
                                  DetailView, 
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

context = {
    'posts' : Post.objects.all(),
}

def home(request):
    return render(request,'home.html',context)

class PostListView(ListView):
    model = Post
    template_name = 'home.html'  #<app>/<model>_<viewtype>.html
    context_object_name = 'posts' 
    # by default refers to a post as object. so instead of changing the name 
    # in template new name can be given to refer it by.
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_forms.html'
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'post_forms.html'
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self) -> bool | None:
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = '/'

    def test_func(self) -> bool | None:
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request,'about.html',{'title' : 'About'})