from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.utils import timezone
from .models import Post, Comment, Tag
from .forms import PostForm, CommentForm, SignupForm, AuthForm
import json
import logging
import configparser


config = configparser.ConfigParser()
config.read('cnf.ini')
logging.basicConfig(
    level=config['LOGGING']['level'],
    filename=config['LOGGING']['filename']
)
log = logging.getLogger(__name__)
def mainPage(request):
    posts = Post.objects.filter(published_date=timezone.now()).order_by('-published_time')
    return render(request, 'blog/post_list.html', {'posts': posts})

def register_user(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            log.info(f'{request.user} registred')
            form.save()
            return redirect('login')
    else:
        form = SignupForm(request.POST)
    return render(request,'register/registration.html',{'form': form})

def login_user(request):
    if request.user.is_authenticated:
        return redirect('main_page')
    if request.method == 'POST':
        form = AuthForm(request, request.POST)
        print("form: ", form.data)
        print('post: ', request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('my_posts', usr=request.user.pk)
    else:
        form = AuthForm()
    return render(request,'register/login.html',{'form': form})

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')

def post_list(request, usr):
    posts = Post.objects.filter(author=usr).order_by('published_time')
    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def my_posts(request, usr):
    posts = Post.objects.filter(author=request.user).order_by('author')
    return render(request, 'blog/my_posts.html', {'posts': posts})

def post_detail(request, usr, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request, usr):
    if request.method == "POST":
        el = json.load(request)
        post = Post()
        post.author = request.user
        post.title = el['title']
        post.text = el['text']
        post.save()
        print(el['tags'])
        for strTag in el['tags']:
            tag = Tag.objects.get(name=strTag)
            post.tags.add(tag)
        log.info(f'{request.user} added a post {post.title}')
        return redirect('post_detail', usr=request.user.pk, pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, usr, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            log.info(f'{request.user} edited a post {post.title}')
            post.author = request.user
            post.publish()
            post.save()
            return redirect('post_detail', usr=request.user.pk,pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request, usr):
    posts = Post.objects.filter(published_time__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, usr, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    log.info(f'{request.user} publish a post {post.title}')
    return redirect('post_detail', usr=request.user.pk, pk=pk)

@login_required
def post_remove(request, usr, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    log.info(f'{request.user} removed a post {post.title}')
    return redirect('post_list', usr=request.user.pk,)

def add_comment_to_post(request, usr, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            log.info(f'{comment.author} added a comment to {comment.post}')
            return redirect('post_detail', usr=request.user.pk, pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, usr, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    log.info(f'{request.user} approved a {comment.author}s comment')
    return redirect('post_detail', usr=request.user.pk, pk=comment.post.pk)

@login_required
def comment_remove(request, usr, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    log.info(f'{request.user} removed a {comment.author}s comment')
    return redirect('post_detail', usr=request.user.pk, pk=comment.post.pk)

@login_required
def add_tag(request):
    x = json.load(request)['message'].replace(' ', '')
    print(len(x))
    if len(x) == 0 or Tag.objects.filter(name=x).exists():
        message = None
    else:
        message = x
        tag = Tag(name=message)
        tag.save()
    print(Tag.objects.all())
    return JsonResponse({'message': message}, status=200)