from django.test import TestCase
from django.urls import reverse
from .models import Letting, Address


class LettingsIndexViewTest(TestCase):
    def test_lettings_index_view_with_no_lettings(self):
        """
        If no lettings exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('lettings_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No lettings are available.")
        self.assertQuerysetEqual(response.context['lettings_list'], [])

    def test_lettings_index_view_with_a_letting(self):
        """
        If a letting exists, it should be displayed on the index page.
        """
        address = Address.objects.create(
            number=123, street='Main St', city='Anytown',
            state='NY', zip_code=12345,
            country_iso_code='USA'
        )
        letting = Letting.objects.create(title='Test Letting', address=address)
        response = self.client.get(reverse('lettings_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, letting.title)
        self.assertQuerysetEqual(
            response.context['lettings_list'],
            ['<Letting: Test Letting>']
        )


class LettingViewTest(TestCase):
    def test_letting_view_with_valid_letting_id(self):
        """
        If the letting exists, it should be displayed on the letting page.
        """
        address = Address.objects.create(
            number=123, street='Main St', city='Anytown',
            state='NY', zip_code=12345,
            country_iso_code='USA'
        )
        letting = Letting.objects.create(title='Test Letting', address=address)
        response = self.client.get(reverse('letting', args=[letting.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, letting.title)
        self.assertContains(response, f'{address.number} {address.street}')

    def test_letting_view_with_invalid_letting_id(self):
        """
        If the letting does not exist, a 404 error should be returned.
        """
        response = self.client.get(reverse('letting', args=[1]))
        self.assertEqual(response.status_code, 404)
