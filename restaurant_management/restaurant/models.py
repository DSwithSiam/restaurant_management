from django.db import models
from django.contrib.auth.models import AbstractUser
import stripe




from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
   
   
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  
        blank=True,
        help_text='The groups this user belongs to.'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set_permissions', 
        blank=True,
        help_text='Specific permissions for this user.'
    )


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owned_restaurants')

class Menu(models.Model):
    name = models.CharField(max_length=255)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')

class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    




stripe.api_key = 'your_stripe_secret_key'

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(MenuItem)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)

    def create_payment_intent(self):
        intent = stripe.PaymentIntent.create(
            amount=int(self.total_amount * 100),
            currency='usd',
            metadata={'integration_check': 'accept_a_payment'},
        )
        self.stripe_payment_intent_id = intent['id']
        self.save()