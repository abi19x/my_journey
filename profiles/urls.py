from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('order_history/<order_number>', views.order_history, name='order_history'),
    path('order_delete/<order_number>', views.soft_delete_order, name='soft_delete_order'),
]