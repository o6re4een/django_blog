from django.shortcuts import redirect, render
from .models import Post, Comments
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .forms import PostForm, RegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator

# Create your views here.


def index(request):
    posts_list = Post.objects.order_by("-id")
    paginator = Paginator(posts_list, 9)  # Разбиваем на страницы по 6 постов
    page_number = request.GET.get("page")  # Получаем номер страницы из запроса
    recent_posts = paginator.get_page(page_number)  # Получаем объект страницы
    return render(request, "post/index.html", {"recent_posts": recent_posts})


def post_detail(request, post_id):
    post = Post.objects.prefetch_related("comments_set", "author").get(pk=post_id)
    return render(request, "post/_post_detail.html", {"post": post})


@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(pk=post_id)
        content = request.POST.get("content")
        if content:
            Comments.objects.create(post=post, author=request.user, content=content)
        else:
            messages.error(request, "Комментарий не может быть пустым.")
        return redirect("post_detail", post_id=post_id)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/post")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


@login_required  # Только авторизованные пользователи могут создавать посты
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Устанавливаем автора поста
            post.save()
            return redirect(
                "post_detail", post_id=post.id
            )  # Перенаправляем на страницу поста
    else:
        form = PostForm()
    return render(request, "post/_create_post.html", {"form": form})


# def login(request):
#     return render(request, "post/login.html")
