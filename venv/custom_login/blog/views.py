from blog.forms import CommentForm
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView,UpdateView,ListView,DetailView,View,TemplateView,DeleteView
from blog.models import Blog, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin 
from blog.forms import CommentForm
from accounts.models import CustomUser

# Create your views here.

class MyBlogs(LoginRequiredMixin, TemplateView):
    template_name = 'blog/my_blog.html'

class UpdateBlog(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ('blog_title','blog_content','blog_image')
    template_name = 'blog/edit_blog.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('blog:blog_details',kwargs={'slug':self.object.slug})


class DeleteBlog(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url ="/blog/my-blogs/"

class CreateBlog(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'blog/create_blog.html'
    fields = ('blog_title', 'blog_content', 'blog_image')

    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        blog_obj.save()
        return HttpResponseRedirect(reverse('blog:blog_list'))

class BlogList(ListView):
    context_object_name = 'blogs'
    model = Blog
    paginate_by = 3
    template_name = 'blog/blog_list.html'

def Individual(request,pk):
    author = CustomUser.objects.get(pk=pk)
    obj = Blog.objects.filter(author = author)

    return render(request,'blog/individual_blog.html',{'obj':obj})

@login_required
def blog_details(request, slug):
    blog = Blog.objects.get(slug= slug)
    comment_form = CommentForm()
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect(reverse('blog:blog_details',kwargs={'slug':slug}))
    return render(request,'blog/blog_details.html',context={'blog':blog,'comment_form':comment_form})
