from django.db import models

class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название"
    )

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    author = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)
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
    text_comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    name_author = models.CharField(max_length=20)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    def __str__(self):
        return self.text_comment

