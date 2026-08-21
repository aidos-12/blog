from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views
from .views import home, post_detail, search, orm_demo


urlpatterns = [
    path("home/", views.home, name="home"),

    path("post/<int:post_id>/", post_detail, name="post_detail"),
    path("post/<int:post_id>/comment/", views.comment_create, name="comment_create"),
    path("post/<int:post_id>/edit/", views.post_update, name="post_update"),
    path("post/<int:post_id>/delete/", views.post_delete, name="post_delete"),

    path("search/", search, name="search"),

    path("contact/<str:name>/", views.contact, name="contact"),
    path("posts/", views.posts, name="posts"),
    path("posts/all/", views.post_list, name="post_list"),

    path("about/", views.about, name="about"),
    path("contacts/", views.contacts, name="contacts"),
    path("", views.index, name="index"),
    path("rules/", views.rules, name="rules"),

    path("orm_demo/", orm_demo, name="orm_demo"),
    path("orm_homework/", views.orm_homework, name="orm_homework"),

    path("post_form/", views.post_form, name="post_form"),

    path("categories/create/", views.category_create, name="category_create"),
    path("categories/", views.category_list, name="category_list"),
    path("category/<int:category_id>/", views.posts_by_category, name="posts_by_category"),
    path("category/<int:category_id>/detail/", views.category_detail, name="category_detail"),
    path("category/<int:category_id>/edit/", views.category_update, name="category_update"),
    path("category/<int:category_id>/delete/", views.category_delete, name="category_delete"),

    path("comments/", views.comment_list, name="comment_list"),
    path("comment/<int:comment_id>/", views.comment_detail, name="comment_detail"),
    path("comment/<int:comment_id>/edit/", views.comment_update, name="comment_update"),
    path("comment/<int:comment_id>/delete/", views.comment_delete, name="comment_delete"),

    path("success/", views.success, name="success"),

    path("register/", views.register, name="register"),
    path("login/",LoginView.as_view(template_name="blog/login.html"),name="login",),
    path("logout/",LogoutView.as_view(next_page="home"),name="logout",),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('my-posts/', views.my_posts, name='my_posts'),
]