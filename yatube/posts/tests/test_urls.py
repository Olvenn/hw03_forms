from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Group, Post

User = get_user_model()


class StaticURLTests(TestCase):
    def setUp(self):
        # Устанавливаем данные для тестирования
        # Создаём экземпляр клиента. Он неавторизован.
        self.guest_client = Client()

    def test_homepage(self):
        # Отправляем запрос через client,
        # созданный в setUp()
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        # Создадим запись в БД для проверки доступности адреса task/test-slug/
        cls.user = User.objects.create_user(username='TestUser')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            description='Тестовое описание',
            slug='test-slug',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем пользователя
        # self.user = User.objects.create_user(username='HasNoName')
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    # def test_home_url_exists_at_desired_location(self):
    #     """Страница / доступна любому пользователю."""
    #     response = self.guest_client.get('/')
    #     self.assertEqual(response.status_code, 200)

    # def test_group_slug_exists_at_desired_location(self):
    #     """Страница / доступна любому пользователю."""
    #     response = self.guest_client.get(f'/group/{self.group.slug}/')
    #     self.assertEqual(response.status_code, 200)

    # def test_posts_post_id_exists_at_desired_location(self):
    #     """Страница / доступна любому пользователю."""
    #     response = self.guest_client.get(f'/posts/{self.post.id}/')
    #     self.assertEqual(response.status_code, 200)

    # def test_posts_username_exists_at_desired_location(self):
    #     """Страница / доступна любому пользователю."""
    #     response = self.guest_client.get(f'/profile/{self.user.username}/')
    #     self.assertEqual(response.status_code, 200)

    def test_str_exists_at_desired_location(self):
        """Страница / доступна любому пользователю."""

        test_items = {
            '/': '/',
            '/group/slug/': f'/group/{self.group.slug}/',
            '/posts/id/': f'/posts/{self.post.id}/',
            '/profile/username/': f'/profile/{self.user.username}/'
        }

        for path, expected_value in test_items.items():
            with self.subTest(path=path):
                self.assertEqual(
                    self.guest_client.get(expected_value).status_code, 200)

    def test_posts_unexisting_page_exists_at_desired_location(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)

    def test_str_exists_at_desired_location_authorized(self):
        """Страница / доступна любому пользователю."""

        test_items = {
            '/posts/id/edit/': f'/posts/{self.post.id}/edit/',
            '/create/': '/create/',
        }

        for path, expected_value in test_items.items():
            with self.subTest(path=path):
                self.assertEqual(
                    self.authorized_client.get(expected_value)
                    .status_code, 200)

    # def test_posts_id_edit_url_exists_at_desired_location_authorized(self):
    #     """Страница /posts/id/edit/ доступна авторизованному
    #     пользователю."""
    #     response = self.authorized_client.get(f'/posts/{self.post.id}/edit/')
    #     self.assertEqual(response.status_code, 200)

    # def test_create_exists_at_desired_location_authorized(self):
    #     """Страница /create/ доступна авторизованному
    #     пользователю."""
    #     response = self.authorized_client.get('/create/')
    #     self.assertEqual(response.status_code, 200)
