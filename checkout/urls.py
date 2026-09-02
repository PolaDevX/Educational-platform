from django.urls import path

from checkout import webhooks
from . import views

urlpatterns = [
    path('stripe', views.stripe_transaction, name='checkout.stripe'),
    path('stripe/config', views.stripe_config, name='checkout.stripe.config'),
    path('stripe/webhook/', webhooks.stripe_webhook),
]