from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .models import Post,Category,Comment
from .form import PostForm,CommentForm,CategoryForm
from django.core.paginator import Paginator

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

# def post_detail(request, post_id):
#     return HttpResponse(f"Пост номер {post_id}")

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

def post_form(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/blog/success/?title=Пост создан&message=Пост успешно добавлен!")

    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request,'blog/post_form.html',{'form': form})

def comment_create(request,post_id):
    post = get_object_or_404(Post, id = post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.post = post
            comment.save()
            return redirect(f'/success/?title=Комментарий добавлен&message=Спасибо за ваш комментарий!')
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form, 'post' : post})


def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/blog/success/?title=Категория создана&message=Новая категория успешно добавлена!")
    else:
        form = CategoryForm()
    return render(request, "blog/category_form.html", {"form": form,})

def success(request):
    return render(request,"blog/success.html",
        {"title": request.GET.get("title", "Успешно!"),
        "message": request.GET.get("message", "Операция выполнена успешно."),},)

def category_list(request):
    categories = Category.objects.all()
    return render(request, "blog/category_list.html", {
        "categories": categories,
    })


def comment_list(request):
    comments = Comment.objects.all()
    return render(request, "blog/comment_list.html", {
        "comments": comments,
    })

def post_list(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "blog/post_list.html", {'page_obj': page_obj})

def posts_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category,is_published=True).order_by('-created_at')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/posts_by_category.html', {'page_obj': page_obj,'category': category,})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'post': post})

def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    return render(request,'blog/category_detail.html',{'category': category})

def category_update(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_detail', category_id=category.id)
    else:
        form = CategoryForm(instance=category)
    return render(request,'blog/category_form.html',
        {'form': form,'category': category})

def category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request,'blog/category_confirm_delete.html',{'category': category})


def comment_detail(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    return render(request,'blog/comment_detail.html',{'comment': comment})


def comment_update(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail',post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    return render(request,'blog/comment_form.html',{'form': form,'comment': comment})


def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        post_id = comment.post.id
        comment.delete()
        return redirect('post_detail',post_id=post_id)
    return render(request,'blog/comment_confirm_delete.html',{'comment': comment})

