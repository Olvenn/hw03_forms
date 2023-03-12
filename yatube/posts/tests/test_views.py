from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class PostViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        # Создадим запись в БД для проверки доступности адреса task/test-slug/
        cls.user = User.objects.create_user(username='TestUser')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.group = Group.objects.create(
            title='Тестовая группа',
            description='Тестовое описание',
            slug='test-slug',
        )

        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый пост',
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем пользователя
        self.user = User.objects.create_user(username='HasNoName')
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
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
            reverse('posts:post_edit', kwargs={'post_id':
                    f'{self.post.id}'}): 'posts/post_create.html'
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