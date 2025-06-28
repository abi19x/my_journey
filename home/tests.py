from django.test import TestCase
from django.urls import reverse


class HomeViewTests(TestCase):
    def test_index_view_returns_status_code_200(self):
        """
        Test that the index view returns a 200 status code and uses the correct template.
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
