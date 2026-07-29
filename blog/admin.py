from django.contrib import admin
from .models import Post
from .models import Category
from .models import Comment

# admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_published', 'is_featured')
    list_filter = ('is_published', 'is_featured')
    search_fields = ('title', 'author')

admin.site.register(Category)

admin.site.register(Comment)
