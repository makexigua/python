from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from .forms import UserRegisterForm, PostForm

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'test_app/home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'账号 {username} 创建成功！请登录。')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'test_app/register.html', {'form': form})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, '文章发布成功！')
            return redirect('blog-home')
    else:
        form = PostForm()
    return render(request, 'test_app/post_form.html', {'form': form})

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, '你没有权限编辑这篇文章')
        return redirect('blog-home')
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, '文章更新成功！')
            return redirect('blog-home')
    else:
        form = PostForm(instance=post)
    return render(request, 'test_app/post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, '你没有权限删除这篇文章')
        return redirect('blog-home')
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, '文章删除成功！')
        return redirect('blog-home')
    
    return render(request, 'test_app/post_delete.html', {'post': post})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'test_app/post_detail.html', {'post': post})