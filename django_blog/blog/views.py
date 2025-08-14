from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.db.models import Q
from taggit.models import Tag


def home(request):
    return render(request, 'blog/home.html')

def posts(request):
    return render(request, 'blog/posts.html')

def register(request):
    return render(request, 'blog/register.html')



# Registration view
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('profile')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('profile')
        else:
            messages.error(request, "Login failed. Please check your username and password.")
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')

# Profile view
@login_required
def profile_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            request.user.email = email
            request.user.save()
            messages.success(request, "Profile updated successfully.")
    return render(request, 'blog/profile.html')



# List all blog posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']  # newest posts first

# Show details of a single post
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

# Create a new post (authenticated users only)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user  # set author automatically
        return super().form_valid(form)

# Update a post (only author)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    
# Tag view
def posts_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = Post.objects.filter(tags__name__in=[tag_name])
    return render(request, 'blog/posts_by_tag.html', {'tag': tag, 'posts': posts})

# Search view
def search_posts(request):
    query = request.GET.get('q')
    results = Post.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(tags__name__icontains=query)
    ).distinct()
    return render(request, 'blog/search_results.html', {'results': results, 'query': query})



# Delete a post (only author)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author




# Adding a new comment
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post-detail', pk=post_id)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})

# Updating a comment
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

# Deleting a comment
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    
    
class CommentCreateView(CreateView):
    model = Comment
    fields = ['content']  # Adjust fields based on your Comment model
    template_name = 'blog/comment_form.html'  # Create this template

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']  # Link comment to the post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['pk']})
