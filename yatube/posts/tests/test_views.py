from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django import forms


from ..models import Group, Post

User = get_user_model()


class PostViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='TestUser')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.group = Group.objects.create(
            title='Тестовая группа',
            description='Тестовое описание',
            slug='test-slug',
        )

        cls.author = User.objects.create_user(
            first_name='Лев',
            last_name='Толстой',
            username='FirstAuthor',
            email='lev@yatube.ru'
        )

        cls.post = Post.objects.create(
            author=cls.author,
            group=cls.group,
            text='Тестовый пост',
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_page_has_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group', kwargs={'slug': f'{self.group.slug}'}):
                'posts/group_list.html',
            reverse('posts:profile', kwargs={'username':
                    f'{self.user.username}'}): 'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id':
                    f'{self.post.id}'}): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_detail', kwargs={'post_id':
                    f'{self.post.id}'}): 'posts/post_detail.html',
        }
        # Проверяем, что при обращении
        # к name вызывается соответствующий HTML-шаблон
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(template)
                self.assertTemplateUsed(response, reverse_name)

    # def test_home_page_correct_template(self):
    #     """URL-адрес использует шаблон deals/home.html."""
    #     response = self.authorized_client.get(reverse('posts:index'))
    #     self.assertTemplateUsed(response, 'posts/index.html')

    def test_create_post_page_show_correct_context(self):
        """Форма добавления поста сформирована с правильным контекстом"""

        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'group': forms.fields.ChoiceField,
            'text': forms.fields.CharField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_fields = response.context['form'].fields[value]
                self.assertIsInstance(form_fields, expected)

    def test_home_page_show_correct_context(self):
        """Пост отображается на главной странице"""
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]

        post_text_0 = first_object.text
        post_group_0 = first_object.group.title
        post_author_0 = first_object.author.username
        self.assertEqual(post_text_0, 'Тестовый пост')
        self.assertEqual(post_group_0, 'Тестовая группа')
        self.assertEqual(post_author_0, 'FirstAuthor')

    def test_home_page_show_correct_context(self):
        """Пост отображается на главной странице"""
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]

        post_text_0 = first_object.text
        post_group_0 = first_object.group.title
        post_author_0 = first_object.author.username
        self.assertEqual(post_text_0, 'Тестовый пост')
        self.assertEqual(post_group_0, 'Тестовая группа')
        self.assertEqual(post_author_0, 'FirstAuthor')

    def test_post_detail_pages_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = (self.authorized_client.get(reverse('posts:post_detail',
                    kwargs={'post_id': f'{self.post.id}'})))
        self.assertEqual(response.context.get('post').group.title,
                         'Тестовая группа')
        self.assertEqual(response.context.get('post').text, 'Тестовый пост')
