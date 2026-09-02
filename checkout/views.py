import math
import stripe
from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from checkout.forms import UserInfoForm
from checkout.models import Transaction, PaymentMethod
from courses.models import Cart, Course, Order, OrderProduct

# Create your views here.

def stripe_config(request):
    return JsonResponse({
        'public_key': settings.STRIPE_PUBLISHABLE_KEY,
    })

@login_required
def stripe_transaction(request):
    transaction = make_transaction(request, PaymentMethod.STRIPE)
    
    if not transaction:
        return JsonResponse({
            'message': _('Please enter valid information')
        }, status=400)
    
    stripe.api_key = settings.STRIPE_SECRET_KEY

    intent = stripe.PaymentIntent.create(
        amount=int(transaction.amount * 100),
        currency=settings.CURRENCY,
        payment_method_types=['card'],
        metadata={
            'transaction': transaction.id,
        }
    )

    return JsonResponse({
        'client_secret': intent['client_secret']
    })


def make_transaction(request, pm):
    if not request.user.is_authenticated:
        return None

    form = UserInfoForm(request.POST)
    if not form.is_valid():
        return None

    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart = Cart.objects.filter(session_id=session_key).last()

    if not cart or not cart.items:
        return None

    courses = Course.objects.filter(pk__in=cart.items)
    total = sum(course.price for course in courses)

    if total <= 0:
        return None

    customer_data = {
        'full_name': request.user.get_full_name() or request.user.username,
        'email': request.user.email,
        'user_id': request.user.id,
    }

    transaction = Transaction.objects.create(
        customer=customer_data,
        session=session_key,
        payment_method=pm,
        items=cart.items,
        amount=math.ceil(total),
    )

    request.session['purchaser_email'] = request.user.email

    return transaction