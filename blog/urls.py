from django.urls import path
from .views import home,post_detail,search,orm_demo
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('search/', search, name='search'),
    path("contact/<str:name>/", views.contact, name="contact"),
    path("posts/", views.posts, name="posts"),
    path("about/", views.about, name="about"),
    path("contacts/", views.contacts, name="contacts"),
    path("", views.index, name="index"),
    path("rules/", views.rules, name="rules"),
    path("orm_demo/",views.orm_demo , name="orm_demo"),
    path("orm_homework/", views.orm_homework, name="orm_homework"),
    path("post_form", views.post_form, name="post_form"),
    path("post/<int:post_id>/comment",views.comment_create,name="comment_create"),
    path("categories/create/",views.category_create,name="category_create"),
    path("success/", views.success, name="success"),
    path("categories/", views.category_list, name="category_list"),
    path("comments/", views.comment_list, name="comment_list"),
    path("posts/all/", views.post_list, name="post_list"),
    path('category/<int:category_id>/',views.posts_by_category,name='posts_by_category'),
    path('post/<int:post_id>/edit/', views.post_update, name='post_update'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('category/<int:category_id>/edit/', views.category_update, name='category_update'),
    path('category/<int:category_id>/delete/', views.category_delete, name='category_delete'),
    path('comment/<int:comment_id>/',views.comment_detail,name='comment_detail'),
    path('comment/<int:comment_id>/edit/',views.comment_update,name='comment_update'),
    path('comment/<int:comment_id>/delete/',views.comment_delete,name='comment_delete'),
]