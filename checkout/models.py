from django.db import models
from django.utils.translation import gettext as _
# Create your models here.


class TransactionStatus(models.IntegerChoices):
    Pending = 0, _('Pending')
    Completed = 1, _('Completed')

class PaymentMethod(models.IntegerChoices):
    STRIPE = 1, _('Stripe')

class Transaction(models.Model):
    session = models.CharField(max_length=255)
    amount = models.FloatField()
    items = models.JSONField(default=dict)
    customer = models.JSONField(default=dict)
    status = models.IntegerField(
        choices=TransactionStatus.choices,
        default=TransactionStatus.Pending
    )
    payment_method = models.IntegerField(
        choices=PaymentMethod.choices,
        default=PaymentMethod.STRIPE  
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def customer_name(self):
        return self.customer['first_name'] + ' ' + self.customer['last_name']
    
    @property
    def customer_email(self):
        return self.customer['email']
    def __str__(self):
        if isinstance(self.customer, dict) and 'full_name' in self.customer:
            return f"Transaction #{self.id} - {self.customer['full_name']}"
        return f"Transaction #{self.id}"