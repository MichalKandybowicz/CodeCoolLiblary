from django.test import TestCase
from django.urls import reverse

from catalog.models import Genre


class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_genre = 13

        for genre_id in range(number_of_genre):
            Genre.objects.create(
                name='Fantasy'
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/genre/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('genre'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('genre'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'genre_list.html')

