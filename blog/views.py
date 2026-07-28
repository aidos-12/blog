from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

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