from django.shortcuts import render

from . models import ShippingAddress, Order, OrderItem

from cart.cart import Cart

from django.http import JsonResponse

from django.core.mail import send_mail

from django.conf import settings

# TAX_RATE = .0575



def checkout(request):

    # users with accounts -- prefill the form

    if request.user.is_authenticated:

        try:

            # Authenticated user WITH shipping info

            shipping_address = ShippingAddress.objects.get(user=request.user.id)

            context = {'shipping':shipping_address}


            return render(request, 'payment/checkout.html', context=context)
        
        except:

            # Authenticated users with no shpping info

            return render(request, 'payment/checkout.html')
        
    else:

         #Guest user
        
        return render(request, 'payment/checkout.html')
        
   

def payment_success(request):

    # Clear shopping cart

    for key in list(request.session.keys()):

        if key == 'session_key':

            del request.session[key]

    
    return render(request, 'payment/payment-success.html')


def payment_failed(request):
    
    return render(request, 'payment/payment-failed.html')



def complete_order(request):

    if request.POST.get('action') == 'post':

        name = request.POST.get('name')
        email = request.POST.get('email')

        address1 = request.POST.get('address1')
        #address2 = request.POST.get('address2')
        city = request.POST.get('city')

        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        #style user shipping address / all in one address

        shipping_address = (address1 + "\n" +
        
        city + "\n" + state + "\n" + zipcode) #address2 +
        
        
    
    # shopping cart information

    cart = Cart(request)
    
    total_cost = cart.get_total() # * TAX_RATE

    #Order Variations
    # 1 Create order -> Account users WITH + WITHOUT shipping information
    # 2 Create order -> Guest users without an account

    #user is authenticated

    if request.user.is_authenticated:

        order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address,
                                     
        amount_paid=total_cost, user=request.user)


        order_id = order.pk

        for item in cart:

            OrderItem.objects.create(order_id=order_id, product=item['product'], quantity=item['qty'],
            
            price=item['price'], user=request.user)


        send_mail('Order recieved', 'Hi! ' + '\n\n' + 'Thank you for placing your order' + '\n\n' +
                
            'View your order below' + '\n\n' + str(all_products) + '\n\n' + 'Total paid: $' +

            str(cart.get_total()), settings.EMAIL_HOST_USER, [email], fail_silently=False,)
                

    # Guest user is not authenticated / no account
            
    else:

        order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address,
                                     
        amount_paid=total_cost)


        order_id = order.pk


        product_list = []

        for item in cart:

            OrderItem.objects.create(order_id=order_id, product=item['product'], quantity=item['qty'],
            
            price=item['price'])

            product_list.append(item['product'])
            


        all_products = product_list

    
    # email order
            
        send_mail('Order recieved', 'Hi! ' + '\n\n' + 'Thank you for placing your order' + '\n\n' +
                
            'View your order below' + '\n\n' + str(all_products) + '\n\n' + 'Total paid: $' +

            str(cart.get_total()), settings.EMAIL_HOST_USER, [email], fail_silently=False,)
              
               
        


    order_success = True

    response = JsonResponse({'success':order_success})

    return response
        



    





