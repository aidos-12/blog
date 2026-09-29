from django.test import TestCase
from .models import Post
from .form import PostForm
from django.urls import reverse
from django.contrib.auth.models import User


class PostListViewTest(TestCase):
    def test_post_list_status_code(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)


class PostModelTest(TestCase):
    def test_post_str(self):
        post = Post.objects.create(title='Test post', content='Text')
        self.assertEqual(str(post), 'Test post')


class PostDetail404Test(TestCase):
    def test_nonexistent_post_returns_404(self):
        response = self.client.get(reverse('post_detail', args=[99999]))
        self.assertEqual(response.status_code, 404)


class PostFormTest(TestCase):
    def test_empty_title_invalid(self):
        form = PostForm(data={"title": "", "content": "Text", "is_published": False})
        self.assertFalse(form.is_valid())


class PostCreateLoginTest(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse('post_form'))
        self.assertEqual(response.status_code, 302)


class PostPermissionTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username="author", password="pass12345")
        self.other_user = User.objects.create_user(username="other", password="pass12345")
        self.post = Post.objects.create(title="Author post", content="Text", author=self.author)

    def test_other_user_cannot_edit(self):
        self.client.login(username="other", password="pass12345")
        response = self.client.get(reverse("post_update", args=[self.post.id]))
        self.assertEqual(response.status_code, 403)