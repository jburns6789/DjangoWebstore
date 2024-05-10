from django.db import models

from django.contrib.auth.models import User


class ShippingAddress(models.Model):


    full_name = models.CharField(max_length=150)

    email = models.EmailField(max_length=150)

    address1 = models.CharField(max_length=150)

    address2 = models.CharField(max_length=150)

    city = models.CharField(max_length=150)

    # Optional

    state = models.CharField(max_length=150, null=True, blank=True)

    zipcode = models.CharField(max_length=150, null=True, blank=True)

    # FK <--- dont want users to have multiple address only to update their own.

    # Take into account authenticated and not authenticated

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    class Meta:

        verbose_name_plural = 'Shipping Address'

    
    def __str__(self):

        return 'Shipping Address - ' + str(self.id)

