from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from checkout.models import Order  # Make sure this import exists
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request
    
    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )        

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'unhandled Webhook received: {event["type"]}',
            status=200)
    
    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        metadata = intent.metadata
        order_number = metadata.get('order_number')  # Assuming you added this metadata when creating the payment intent

        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            # Give it a few seconds in case the order hasn't saved to DB yet
            for attempt in range(5):
                time.sleep(1)
                try:
                    order = Order.objects.get(order_number=order_number)
                    break
                except Order.DoesNotExist:
                    order = None

        if order:
            self._send_confirmation_email(order)
    
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
    
    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)