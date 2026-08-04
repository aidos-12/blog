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
]
