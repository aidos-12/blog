from django import forms
from .models import Post, Comment, Category, Profile

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'is_published', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10,'cols': 60}),}

    def clean_image(self):
            image = self.cleaned_data.get('image')
            if image and image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Размер изображения не должен превышать 5 МБ.')
            return image
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text_comment', 'image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and image.size > 3 * 1024 * 1024:
            raise forms.ValidationError('Размер изображения не должен превышать 3 МБ.')
        return image


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar','bio']