from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Post,Category,Comment

def home(request):
    context = {"title": "Main page in my blog"}
    return render(request, "home.html", context)

def index(request):
    return render(request, "home.html")

def about(request):
    context = {"title": "About"}
    return render(request, "about.html", context)

def contacts(request):
    context = {"title": "Contacts"}
    return render(request, "contacts.html", context)

def rules(request):
    context = {"title": "Rules"}
    return render(request, "rules.html", context)

def post_detail(request, post_id):
    return HttpResponse(f"Пост номер {post_id}")

def search(request):
    query = request.GET.get("q", "")
    return HttpResponse(f"Вы искали: {query}")

def contact(request, name):
    return HttpResponse(f"Здравствуйте, {name}! Это страница контактов.")

def posts(request):
    category = request.GET.get("category")

    if category == "news":
        return HttpResponse("Категория: Новости")
    elif category == "tech":
        return HttpResponse("Категория: Технологии")
    else:
        return HttpResponse("Все публикации")


def orm_demo(request):
    all_posts = Post.objects.all()
    published_posts = Post.objects.filter(is_published = True)
    post_sort = Post.objects.filter(views_count__gt = 0).order_by('-views_count')

    result = "All posts:\n"
    for post in all_posts:
        result += f'- {post.title}\n'

    result += "\n Only published posts:\n"
    for post in published_posts:
        result += f'- {post.title}\n'

    category = Category.objects.last()
    if category:
        result += f'\n Post category <<{category.name}>>:\n'
        for post in category.posts.all():
            result += f'- {post.title}\n'
    

    post = Post.objects.first()
    if post:
        result += f"\n Post Comments <<{post.title}>>:\n"
        for comment in post.comments.all():
            result += f"- {comment.name_author}: {comment.text_comment}\n"

    result += "посты по убыванию и больше нуля:"
    for post in post_sort:
        result += f'\n {post.title} : {post.views_count}'

    return HttpResponse(f'<pre>{result}</pre>')


def orm_homework(request):
    all_posts = Post.objects.all()
    published_posts = Post.objects.filter(is_published=True)
    category = Category.objects.first()
    posts_count = Post.objects.count()
    post_sort = Post.objects.order_by('-created_at')

    result = "1. Все посты:\n"
    for post in all_posts:
        result += f"- {post.title}\n"

    result += "\n2. Опубликованные посты:\n"
    for post in published_posts:
        result += f"- {post.title}\n"

    result += "\n3. Посты одной категории:\n"
    if category:
        result += f"Категория: {category.name}\n"
        for post in category.posts.all():
            result += f"- {post.title}\n"

    result += f"\n4.Количество постов: {posts_count}\n"

    result += "\n5.Посты отсортированные по дате создания:\n"
    for post in post_sort:
        result += f"- {post.title} ({post.created_at})\n"

    return HttpResponse(f"<pre>{result}</pre>")