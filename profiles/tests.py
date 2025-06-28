from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from checkout.models import Order
from profiles.models import UserProfile


class UserProfileSignalTests(TestCase):
    def test_user_profile_created_on_user_creation(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.assertTrue(UserProfile.objects.filter(user=user).exists())


class ProfileViewTests(TestCase):
    def test_profile_view_get(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        response = self.client.get(reverse('profile'))  # Adjust URL name if different
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')


class OrderHistoryViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = UserProfile.objects.get(user=self.user)
        self.order = Order.objects.create(
            order_number='TEST12345',
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            country='GB',
            postcode='AB12CD',
            town_or_city='Testville',
            street_address1='123 Test Street',
            original_bag='{}',
            stripe_pid='test_pid_123',
            user_profile=self.profile,
        )

    def test_order_history_view(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('order_history', args=[self.order.order_number])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        self.assertContains(response, 'TEST12345')  # Confirm the order number is in the response


class SoftDeleteOrderViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.profile = UserProfile.objects.get(user=self.user)

        self.order = Order.objects.create(
            order_number='ORDER123',
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            country='GB',
            postcode='AB1 2CD',
            town_or_city='Test Town',
            street_address1='123 Test Street',
            user_profile=self.profile,
        )

    def test_soft_delete_order_as_owner_soft_deletes_order(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('soft_delete_order', args=[self.order.order_number]))

        self.order.refresh_from_db()
        self.assertTrue(self.order.deleted)
        self.assertRedirects(response, reverse('profile'))