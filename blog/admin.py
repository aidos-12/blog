from django.contrib import admin
from .models import Post, Category, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author','category', 'created_at', 'is_published', 'is_featured')
    list_filter = ('is_published', 'is_featured')
    search_fields = ('title', 'author')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text_comment',)