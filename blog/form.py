from django import forms
from .models import Post,Comment,Category

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content','is_published']

        widgets = {
            'content': forms.Textarea(
                attrs={
                    'rows': 8,
                    'cols': 60,
                }
            ),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text_comment']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']