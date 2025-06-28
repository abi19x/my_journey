from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.conf import settings

import stripe

@override_settings(
    STRIPE_PUBLIC_KEY='pk_test_12345',
    STRIPE_SECRET_KEY='sk_test_12345',
    STRIPE_CURRENCY='gbp'
)
class CheckoutViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_checkout_view_get_request_renders_checkout_template(self):
        response = self.client.get(reverse('checkout'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        self.assertIn('order_form', response.context)
        self.assertIn('stripe_public_key', response.context)
        self.assertIn('client_secret', response.context)

