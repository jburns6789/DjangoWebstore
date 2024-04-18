from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms


class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True #mark email as manditory

    # Email validation to ensure uniqueness

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is invalid')
        
        #len function updated
        
        if len(email) >= 350:
            raise forms.ValidationError("Your email is too long")
        
        return email