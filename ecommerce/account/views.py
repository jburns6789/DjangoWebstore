from django.shortcuts import redirect, render
from django.contrib.auth.models import User

from .forms import CreateUserForm, LoginForm, UpdateUserForm

from payment.forms import ShippingForm # form output on the form, logic is in this view
from payment.models import ShippingAddress # model make queries
from payment.models import Order, OrderItem

from django.contrib.sites.shortcuts import get_current_site
from . token import user_tokenizer_generate

from django.template.loader import render_to_string
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from django.contrib import messages


def register(request):

    form = CreateUserForm()

    if request.method == 'POST':

        form = CreateUserForm(request.POST)

        if form.is_valid():

            user = form.save()

            user.is_active = False

            user.save()

            # email verification setup

            current_site = get_current_site(request)

            subject = 'Account Verification Email'

            message = render_to_string('account/registration/email-verification.html', 

            {
                'user': user, 
                'domain': current_site.domain ,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user),


            })
            
            user.email_user(subject=subject, message=message)            

            return redirect ('email-verification-sent')
        
    context = {'form':form}

    return render(request, 'account/registration/register.html', context=context)


def email_verification(request, uidb64, token):

    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)

    # success
    if user and user_tokenizer_generate.check_token(user, token):

        user.is_active = True

        user.save()

        return redirect('email-verification-success')

    # failed

    else:
        
        return redirect('email-verification-failed')


def email_verification_sent(request):
    
    return render(request, 'account/registration/email-verification-sent.html')


def email_verification_success(request):
    
    return render(request, 'account/registration/email-verification-success.html')


def email_verification_failed(request):
    
    return render(request, 'account/registration/email-verification-failed.html')



def my_login(request):

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)

                return redirect("dashboard")
            
    context = {"form": form}

    return render(request, "account/my-login.html", context=context)


# Logout

def user_logout(request):

    # adding persisting cart session

    try:

        for key in list(request.session.keys()):

            if key == 'session_key':

                continue
        
        else:

            del request.session[key]

    except KeyError:

        pass

    messages.success(request, "Logout success!")
    # were ever you redirect to that is where you must put the html template
    # look at the base html at the bottom

    return redirect("store")


# Login

@login_required(login_url='my-login')
def dashboard(request):
    
    return render(request,'account/dashboard.html')


# Profile management

@login_required(login_url='profile-management')
def profile_management(request):

    # Updating our username and email

    user_form = UpdateUserForm(instance=request.user) # <----- django default validation

    if request.method == 'POST':

        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():

            user_form.save()

            messages.success(request, "Account updated")

            return redirect('dashboard')
        

    user_form = UpdateUserForm(instance=request.user)

    context = {'user_form':user_form}


    return render(request, 'account/profile-management.html', context=context)

# Delete profile

@login_required(login_url='delete-account')
def delete_account(request):

    # Deleting user

    user = User.objects.get(id=request.user.id)

   
    if request.method == 'POST':

        user.delete()

        messages.info(request, "Account deleted")

        return redirect('store')
        
    
    return render(request, 'account/delete-account.html')



# Shipping view

@login_required(login_url='my-login')
def manage_shipping(request):

    try:

        # Account user with shipment info

        shipping = ShippingAddress.objects.get(user=request.user.id) 

    except ShippingAddress.DoesNotExist:

        # Account user without shipment info

        shipping = None

    
    form = ShippingForm(instance=shipping)
    
    if request.method == 'POST':

        form = ShippingForm(request.POST, instance=shipping)

        if form.is_valid():

            # Assign the user FK on the object

            shipping_user = form.save(commit=False)

            # Adding the FK itself

            shipping_user.user = request.user

            shipping_user.save()

            return redirect('dashboard')
        
    context = {'form':form}

    return render(request, 'account/manage-shipping.html', context=context)


@login_required(login_url='my-login')
def track_orders(request):

    try:
        orders = OrderItem.objects.filter(user=request.user)

        context = {'orders':orders}

        return render(request, 'account/track-orders.html', context=context)

    except:

        return render(request, 'account/track-orders.html')
