from django.core.validators import RegexValidator
from django.db import models
from apps.products.models import Product
from apps.commons.models import BaseModel
from apps.users.models import User
phone_regex = RegexValidator(
    regex=r'^998[0-9]{9}$',
    message="Phone number must be entered in the format: '998 [XX] [XXX XX XX]'. Up to 12 digits allowed."
)


# Create your models here.
class Order(BaseModel):

    CASH, CARD = 'Cash', 'Card'
    PAYMENT_TYPES = ((CASH, 'Cash'), (CARD, 'Card'))

    PENDING = 'Pending'
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELED = 'Canceled'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled'),
    ]

    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=13, validators=[phone_regex])
    location = models.CharField(max_length=511, null=True)
    payment_type = models.CharField(choices=PAYMENT_TYPES, default=CARD)
    status = models.CharField(choices=STATUS_CHOICES, default=PENDING)
    is_paid = models.BooleanField(default=False)

    def set_status(self, new_status):
        if new_status not in dict(self.STATUS_CHOICES):
            raise ValueError("Invalid status")
        self.status = new_status
        self.save()

    def is_transition_allowed(self, new_status):
        allowed_transitions = {
            self.PENDING: [self.PROCESSING, self.CANCELED],
            self.PROCESSING: [self.SHIPPED, self.CANCELED],
            self.SHIPPED: [self.DELIVERED, self.CANCELED],
        }

        return new_status in allowed_transitions.get(self.status, [])

    def __str__(self):
        return self.phone_number


class OrderProduct(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)

