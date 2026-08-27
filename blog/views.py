from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from .models import Post, Category, Comment, Profile
from .form import PostForm, CommentForm, CategoryForm, ProfileForm, EmailRegisterForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta

RESEND_COOLDOWN_SECONDS = 60


def home(request):
    return render(request, "home.html", {"title": "Main page in my blog"})


def index(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html", {"title": "About"})


def contacts(request):
    return render(request, "contacts.html", {"title": "Contacts"})


def rules(request):
    return render(request, "rules.html", {"title": "Rules"})


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
    published_posts = Post.objects.filter(is_published=True)
    post_sort = Post.objects.filter(views_count__gt=0).order_by("-views_count")

    result = "All posts:\n"

    for post in all_posts:
        result += f"- {post.title}\n"

    result += "\nOnly published posts:\n"

    for post in published_posts:
        result += f"- {post.title}\n"

    category = Category.objects.last()

    if category:
        result += f"\nPost category <<{category.name}>>:\n"
        for post in category.posts.all():
            result += f"- {post.title}\n"

    post = Post.objects.first()

    if post:
        result += f"\nPost Comments <<{post.title}>>:\n"
        for comment in post.comments.all():
            result += f"- {comment.name_author}: {comment.text_comment}\n"

    result += "\nПосты по убыванию и больше нуля:"

    for post in post_sort:
        result += f"\n{post.title}: {post.views_count}"

    return HttpResponse(f"<pre>{result}</pre>")


def orm_homework(request):
    all_posts = Post.objects.all()
    published_posts = Post.objects.filter(is_published=True)
    category = Category.objects.first()
    posts_count = Post.objects.count()
    post_sort = Post.objects.order_by("-created_at")

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

    result += f"\n4. Количество постов: {posts_count}\n"
    result += "\n5. Посты отсортированные по дате создания:\n"

    for post in post_sort:
        result += f"- {post.title} ({post.created_at})\n"

    return HttpResponse(f"<pre>{result}</pre>")


@login_required
def post_form(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/success/?title=Пост создан&message=Пост успешно добавлен!")
    else:
        form = PostForm()

    return render(request, "blog/post_form.html", {"form": form})


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("home")
    else:
        form = PostForm()

    return render(request, "blog/post_form.html", {"form": form})


@login_required
def comment_create(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.name_author = request.user.username
            comment.save()
            return redirect("post_detail", post_id=post.id)
    else:
        form = CommentForm()

    return render(request, "blog/comment_form.html", {"form": form, "post": post})


def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/blog/success/?title=Категория создана&message=Новая категория успешно добавлена!")
    else:
        form = CategoryForm()

    return render(request, "blog/category_form.html", {"form": form})


def success(request):
    return render(request, "blog/success.html", {
        "title": request.GET.get("title", "Успешно!"),
        "message": request.GET.get("message", "Операция выполнена успешно.")
    })


def category_list(request):
    categories = Category.objects.all()
    return render(request, "blog/category_list.html", {"categories": categories})


def comment_list(request):
    comments = Comment.objects.all()
    return render(request, "blog/comment_list.html", {"comments": comments})


def post_list(request):
    posts = Post.objects.filter(is_published=True).order_by("-created_at")
    paginator = Paginator(posts, 5)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "blog/post_list.html", {"page_obj": page_obj})


def posts_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category, is_published=True).order_by("-created_at")
    paginator = Paginator(posts, 5)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "blog/posts_by_category.html", {"page_obj": page_obj, "category": category})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "blog/post_detail.html", {"post": post})


@login_required
def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("Вы не можете редактировать чужой пост")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            return redirect("post_detail", post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, "blog/post_form.html", {"form": form, "post": post})


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("Вы не можете удалить чужой пост")

    if request.method == "POST":
        post.delete()
        return redirect("post_list")

    return render(request, "blog/post_confirm_delete.html", {"post": post})


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    return render(request, "blog/category_detail.html", {"category": category})


def category_update(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            return redirect("category_detail", category_id=category.id)
    else:
        form = CategoryForm(instance=category)

    return render(request, "blog/category_form.html", {"form": form, "category": category})


def category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        category.delete()
        return redirect("category_list")

    return render(request, "blog/category_confirm_delete.html", {"category": category})


def comment_detail(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    return render(request, "blog/comment_detail.html", {"comment": comment})


@login_required
def comment_update(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.name_author != request.user.username:
        return HttpResponseForbidden("Вы не можете редактировать чужой комментарий")

    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES, instance=comment)

        if form.is_valid():
            form.save()
            return redirect("post_detail", post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, "blog/comment_form.html", {
        "form": form,
        "post": comment.post,
        "comment": comment
    })


@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.name_author != request.user.username:
        return HttpResponseForbidden("Вы не можете удалить чужой комментарий")

    if request.method == "POST":
        comment.delete()
        return redirect("post_detail", post_id=comment.post.id)

    return render(request, "blog/comment_confirm_delete.html", {"comment": comment})


@login_required
def profile_view(request):
    return render(request, "blog/profile.html", {"profile_user": request.user})


@login_required
def profile_edit(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "blog/profile_edit.html", {"form": form})


@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, "blog/my_posts.html", {"posts": posts})


def send_confirmation_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    confirm_url = request.build_absolute_uri(f"/confirm-email/{uid}/{token}/")

    print(f"\n>> ССЫЛКА ПОДТВЕРЖДЕНИЯ ДЛЯ {user.email}: {confirm_url}\n")

    message = render_to_string("blog/email_confirmation_message.html", {
        "user": user,
        "confirm_url": confirm_url
    })

    send_mail(
        subject="Подтверждение регистрации в Blog System",
        message=message,
        from_email=None,
        recipient_list=[user.email]
    )

    user.profile.last_confirmation_sent = timezone.now()
    user.profile.save()


def register(request):
    if request.method == "POST":
        form = EmailRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_confirmation_email(request, user)
            return redirect("registration_pending")
    else:
        form = EmailRegisterForm()

    return render(request, "blog/register.html", {"form": form})


def registration_pending(request):
    return render(request, "blog/registration_pending.html")


def confirm_email(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "blog/email_confirmed.html")

    return render(request, "blog/email_confirmation_invalid.html")


def resend_confirmation(request):
    error = None

    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email, is_active=False)
            last_sent = user.profile.last_confirmation_sent

            if last_sent and timezone.now() < last_sent + timedelta(seconds=RESEND_COOLDOWN_SECONDS):
                seconds_left = int((last_sent + timedelta(seconds=RESEND_COOLDOWN_SECONDS) - timezone.now()).total_seconds())
                error = f"Письмо уже отправлялось недавно. Подождите ещё {seconds_left} сек."
            else:
                send_confirmation_email(request, user)

            return redirect("registration_pending")

        except User.DoesNotExist:
            error = "Пользователь с таким email не найден или уже зарегистрирован."

    return render(request, "blog/resend_confirmation.html", {"error": error})