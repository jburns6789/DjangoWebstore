from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms

from django.forms.widgets import PasswordInput, TextInput


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
    

# Login Form

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())



# Update Form
class UpdateUserForm(forms.ModelForm):
    
    password = None

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True #mark email as manditory


    class Meta:
        model = User

        fields = ['username', 'email']
        exclude = ['password1', 'password1']



# class DeleteUserForm(forms.ModelForm):

#     password = None

#     class Meta:
#         model = User

#         fields = ['username', 'email']
#         exclude = ['password1', 'password1']

