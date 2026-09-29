from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from django.contrib import messages

from django.views.generic import DetailView,UpdateView,CreateView,ListView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Profile,Post,Comment ,Category
from .forms import RegisterForm,ProfileForm,PostForm,CommentForm
# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # password hashing
            User.objects.create_user(
                username=username, 
                email=email,
                password=password,
            )
            return redirect('login')
    else:
        form = RegisterForm()
    context = {'form': form,}
    return render(request, 'accounts/register.html',context )

@login_required
def home_view(request):
    return render(request, 'pages/home.html')


#    LoginRequiredMixin beyedman en el user lazem yeb'a 3mel login            
class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'pages/profile.html'


    def get_object(self):  #23red el profile beta3 el current user
        return self.request.user.profile

class ProfileUpdateView(LoginRequiredMixin,UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'pages/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile

class PostCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Post
    form_class = PostForm
    template_name = 'pages/post_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user  #auther howa el loggedin user
        messages.success(self.request,'Post created successfully! ')
        return super().form_valid( form)
    def test_func(self):
        return self.request.user.has_perm('accounts/add_post')

class PostListView(ListView):
    model = Post
    template_name = 'pages/post_list.html'
    context_object_name = 'posts'  # 3shan lamma tegy t3mel 3leeha loop
    paginate_by = 5

class PostDetailView(DetailView):
    model = Post
    template_name = 'pages/post_detail.html'


def category_posts_view(request,pk):
    category = get_object_or_404( Category ,pk=pk)
    posts = get_object_or_404(Post , category=category)
    context = {
        'category':category,
        'posts':posts
    }

    return render(request, 'pages/category_posts.html', context)


class MyPostsView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'pages/my_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(
            author = self.request.user
        )

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'pages/post_form.html'
    success_url = reverse_lazy('post_list')
    def test_func(self):
        post = self.get_object()  #get the user
        return (
            post.author == self.request.user and self.request.user.has_perm('accounts.change_post')
            ) #if True allow to edit
    def form_valid(self, form):
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)


class DeletePostView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    template_name = 'pages/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    def delete(self, request, *args, **kwargs):
        messages.success(
            self.request,
            'Post deleted successfully!'
        )
        return super().delete(request, *args, **kwargs)
    def test_func(self):
        post = self.get_object()
        return (post.author == self.request.user and self.request.user.has_perm('accounts.delete_post'))

@login_required
def add_comment(request,pk):
    post = Post.objects.get(pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            messages.success(
            request,
            'Comment added successfully!'
            )

            return redirect('post_detail', pk=post.pk)
    else:
        form =CommentForm()

    return render(request, 'pages/comment_form.html', {'form':form, 'post':post})

class CommentUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'pages/comment_form.html'

    def test_func(self):
        comment = self.get_object()  #user le 3mal comment
        return comment.user == self.request.user
    
    def form_valid(self, form):
        messages.success(
            self.request,
            'Comment updated successfully!'
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail',kwargs = {'pk':self.object.post.pk })


class CommentDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'pages/comment_confirm_delete.html'
    def test_func(self):
        comment = self.get_object()
        return comment.user == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(
            self.request,
            'Comment deleted successfully!'
        )
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('post_detail',kwargs = {'pk':self.object.post.pk })

def search_view(request):
    query = request.GET.get('q','')
    if query:
        posts = Post.objects.filter(title__icontains=query)
    else:
        posts = Post.objects.none()

    context={
        'posts':posts,
        'query':query
    }

    return render(request,'pages/search.html',context)