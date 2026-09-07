from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.http import HttpResponse
from checkout import models
from courses.models import Order, Course
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.models import User
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

@csrf_exempt
def stripe_webhook(request):
    print('stripe webhook')
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')


    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
        )
    except ValueError as e:
        print('Invalid payload')
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print('Invalid signature')
        return HttpResponse(status=400)

    if event and event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
        print('payment_intent.succeeded')
        print(payment_intent.metadata)
        transaction_id = payment_intent.metadata['transaction']
        make_order(transaction_id)
    else:
        print('Unhandled event type {}'.format(event['type']))

    return HttpResponse(status=200)

def make_order(transaction_id):
    transaction = models.Transaction.objects.get(pk=transaction_id)

    # منع إنشاء Order مكرر
    if transaction.status == models.TransactionStatus.Completed:
        return

    courses = Course.objects.filter(pk__in=transaction.items)

    total = sum(course.price for course in courses)

    customer_data = transaction.customer or {}
    customer_email = customer_data.get('email')

    user = User.objects.filter(email=customer_email).first()

    if not user:
        print(f'User not found for email: {customer_email}')
        return

    order = Order.objects.create(
        transaction=transaction,
        user=user,
        customer=customer_data,
        total=total,
        status='completed'
    )

    order.courses.set(courses)

    transaction.status = models.TransactionStatus.Completed
    transaction.save(update_fields=['status'])

    for course in courses:
        order.orderproduct_set.create(
            course_id=course.id,
            price=course.price
        )

    customer_email = customer_data.get('email')

    if customer_email:
        msg_html = render_to_string('emails/order.html', {
            'order': order,
            'courses': courses,
        })

        send_mail(
            subject='Order Completed',
            html_message=msg_html,
            message=msg_html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[customer_email],
        )