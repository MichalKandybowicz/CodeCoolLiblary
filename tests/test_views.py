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

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('genre'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['genre_list']) == 10)

    def test_lists_all_authors(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('genre') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)  # (if cond is True / if cond: )
        self.assertTrue(len(response.context['genre_list']) == 3)
