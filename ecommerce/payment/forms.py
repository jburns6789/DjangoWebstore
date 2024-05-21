from django import forms

from . models import ShippingAddress

class ShippingForm(forms.ModelForm):

    class Meta:

        model = ShippingAddress

        fields = ['full_name', 'email', 'address1', 'city', 'state', 'zipcode'] #address2,
        exclude = ['user',]