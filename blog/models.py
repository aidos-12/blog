from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    author = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100)

    # def __str__(self):
    #     return f'{self.name} : ({self.created_at})'


class Comment(models.Model):
    text_comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    name_author = models.CharField(max_length=20)

    def __str__(self):
        return self.text_comment