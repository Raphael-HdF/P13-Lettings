from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Profile


class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            favorite_city='Paris'
        )

    def test_profiles_index_view(self):
        url = reverse('profiles_index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles_index.html')
        self.assertContains(response, self.user.username)

    def test_profile_view(self):
        url = reverse('profile', args=[self.user.username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.profile.favorite_city)

    def test_profile_view_with_invalid_username(self):
        url = reverse('profile', args=['wrong_user'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_profile_model(self):
        self.assertEqual(str(self.profile), self.user.username)
