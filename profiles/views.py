from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden

from .models import UserProfile
from .forms import UserProfileForm

from checkout.models import Order


def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
             form.save()
             messages.success(request, 'Profile updated successfully')

    form = UserProfileForm(instance=profile)
    orders = profile.orders.filter(deleted=False)

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
    }
    
    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for donation number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


def soft_delete_order(request, order_number):
    """ Soft delete a user's order from their profile """
    order = get_object_or_404(Order, order_number=order_number)

    if order.user_profile and order.user_profile.user == request.user:
        order.deleted = True
        order.save()
        messages.success(request, f"Donation {order_number} removed from your profile.")
    else:
        return HttpResponseForbidden("You are not authorized to delete this order.")

    return redirect('profile')