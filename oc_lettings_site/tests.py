from django.test import TestCase
from django.urls import reverse


def test_dummy():
    assert 1


class IndexTestCase(TestCase):
    def test_index_view(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Holiday Homes')
