from django.shortcuts import render

def home(request):
    return render(request, 'blog/home.html')

def posts(request):
    return render(request, 'blog/posts.html')

def login_view(request):
    return render(request, 'blog/login.html')

def register(request):
    return render(request, 'blog/register.html')
