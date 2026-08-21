from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название"
    )

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        allow_unicode=True
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    image = models.ImageField(
        upload_to='comments/',
        blank=True,
        null=True
    )
    text_comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    name_author = models.CharField(max_length=20)

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    def __str__(self):
        return self.name_author


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/',blank=True, null=True)

    def __str__(self):
        return self.user.username