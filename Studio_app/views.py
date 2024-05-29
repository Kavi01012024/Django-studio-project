from django.shortcuts import render,redirect
from Studio_app import forms
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import random as r
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.contrib.auth.models import User
from .models import *
from django.http import JsonResponse
import razorpay
from Studio_website_project import settings



# Create your views here.

def home(request):
    print(request.user)
    return render(request,"home.html")

def About_us(request):
    return render(request,"about_us.html")


def bookings(request):
    return render(request,"yourbookings.html")

def signin(request):
    if request.user.is_authenticated:
        print('inside authhhhhhhhhhhhhhhhhhhhhh--------------------------------')
        return render(request,'home.html')
    
    form = forms.CreateUserForms()
    print('entering into signin')

    if request.method == "POST":
        form = forms.CreateUserForms(request.POST)
        u = request.POST['username']
        p = request.POST['password2']
        user_exist = User.objects.filter(username=u).exists()
        print(user_exist)
        if user_exist:
            for_del = User.objects.get(username = u)
            print("fro del",for_del.is_active)
            if for_del.is_active == False:
                for_del = User.objects.get(username = u)
                for_del.delete()

        user = authenticate(request,username = u,password=p)
        print("thi is trheeeeeeeeeeee-------------------",user)

        if user is not None:
            print("to see the user is active or not",user.is_active)
            login(request,user)
            return render(request,'home.html')
            
        else:
            messages.error(request,"username or password incorrect")


    return render(request,"login.html",{'form': form})

def send_maill(request,form = None):

    # for key in request.session.keys(): 
    #     print("request.session key,value =", key,":",request.session[key])

    # print("request.user :",request.user)
    # print("ver_number:",request.session['v_num'])

    if request.method == "POST" and "e_input" in request.POST:

        v_form = forms.Email_verification_form()
        entered_number = request.POST["e_input"]


        if entered_number == request.session['v_num']:

            user = User.objects.get(username=request.session['u_name'])
            user.is_active = True
            user.save()
            login(request,user)
            for key in request.session.keys(): 
                print("request.session key,value =", key,":",request.session[key])
            print("request.user :",request.user)
            return render(request,'home.html')
   
        else:
            messages.error(request,"wrong otp entered,Enter the correct otp u bugger")
        
    else:

        subject = 'Verification Mail'
        message = f'Hi Jobi, thank you for registering in Studio.this is ur Verification number {request.session["v_num"]}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.session['email']]

        send_mail( subject, message, email_from, recipient_list)
        print("mail_sent")
        v_form = forms.Email_verification_form()

    return render(request,"email_verify.html",{"v_f":v_form})





def logup(request):
    
    if request.method == "POST":
        for key,value in request.POST.items():
            print(key,"=",value)

        form = forms.CreateUserForms(request.POST)

        user_exist = User.objects.filter(username=request.POST['username']).exists()
        print(user_exist)
        if user_exist:
            for_del = User.objects.get(username = request.POST['username'])
            print("fro del",for_del.is_active)
            if for_del.is_active == False:
                for_del = User.objects.get(username = request.POST['username'])
                for_del.delete()

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            verification_number = r.randint(60000,70000)
            request.session['v_num'] = str(verification_number)
            request.session['u_name'] = str(form.cleaned_data['username'])
            request.session['email'] = form.cleaned_data['email']
            return send_maill(request)
        print(form.errors)

    else:

        form = forms.CreateUserForms()
        
    return render(request,"logup.html",{'form': form})


def logout_view(request):

    logout(request)

    print("------------this is from logout----------")

    for key in request.session.keys(): 
        print("request.session key,value =", key,":",request.session[key])
    print("request.user :",request.user)
    print('-----------logout success--------------')

    return render(request,'home.html')


def pr_list(request):
    
    products = Product.objects.all()
    for p in products:
        print(p.product_name)
    return render(request,'product_list_page.html',{'products':products})

def pr_desc(request,p_id):

    product = Product.objects.get(id=p_id)
    return render(request,'product_desc_page.html',{"product":product})

def add_to_cart(request):

    user = request.user
    product = Product.objects.get(id=request.GET['p_id'])
    print('name of the product =',product.product_name)

    # logic to increase the quantity and cal total amount
    cart_item = Cart.objects.filter(product=product).filter(user=user).first()

    if cart_item is None:
        new_cart_obj = Cart.objects.create(user=user,product=product,quantity=int(request.GET['quantity']))
        new_cart_obj.save()
    else:
        cart_item.quantity += int(request.GET['quantity'])
        cart_item.save()

    cart_total_tuple = Cart_total.objects.get_or_create(user = user)
    print(type(cart_total_tuple[0]))

    cart_total_tuple[0].total_amount = cart_total_tuple[0].total_amount + (product.product_price * int(request.GET['quantity'])) 
    cart_total_tuple[0].save()
    print('total amount -------------------------------------', cart_total_tuple[0].total_amount)
    return JsonResponse({'message':'success'})
    # logic to increase the quantity and cal total amount -----ends------

    

def go_cart_page(request):

    user_cart = Cart.objects.filter(user = request.user)
    cart_total_amount = Cart_total.objects.get(user = request.user)
    print('of the this shit-----------------------------------------',type(cart_total_amount))
    print('of the this shit-----------------------------------------',cart_total_amount.total_amount)
    return render(request,'cart_page.html',{'user_cart' : user_cart,'cart_total_obj':cart_total_amount})

def remove_cart_item(request):

    cart_id = request.GET["cart_id"]
    print('cart is -------------------------- ',cart_id)
    cart_item = Cart.objects.get(id=cart_id)
    cart_total_obj = Cart_total.objects.get(user = request.user)
    cart_total_obj.total_amount = cart_total_obj.total_amount - (cart_item.product.product_price * cart_item.quantity)
    cart_total_obj.save()
    print('cattotalamount------------------------',cart_total_obj.total_amount)
    cart_item.delete()
    return JsonResponse({'total':cart_total_obj.total_amount})


def address(request):
    saved_address = Addresses.objects.filter(user = request.user)
    address_form = forms.Addresses_form()
    if request.method == "POST":

        if 'address' in request.POST:
            request.session['address_id'] = request.POST['address']
            return redirect('create_order')
        
        address_form = forms.Addresses_form(request.POST)

        if address_form.is_valid():
            name = address_form.cleaned_data['name']
            phone = address_form.cleaned_data['phone']
            print(phone)
            address = address_form.cleaned_data['addr1'] + address_form.cleaned_data['addr2']
            pincode = address_form.cleaned_data['pincode']
            new_address = Addresses.objects.create(name=name, phone=phone, user = request.user, address= address, pincode=pincode,)
            new_address.save()
            request.session['address_id'] = new_address.id
            return redirect('create_order')
        
    data = {'saved_address':saved_address,'address_form':address_form}
    return render(request, 'address.html', data)


def place_order(request):

    return render(request,'place_order.html')

def send_quantity_cart(request):
    cart_items = Cart.objects.filter(user = request.user)
    quantity = 0
    for cart_item in cart_items:
        quantity = quantity + cart_item.quantity
    return JsonResponse({'quantity':quantity})

def payment_success_fail(request):

    if request.POST['status']:
        print('--------------------------------------------vettri')
    return redirect('successFail.html')

def profile_page(request):

    return render(request,'profile.html')


def create_order(request):
    cart_items = Cart.objects.filter(user = request.user)
    if cart_items.exists() == False:
        return render(request,'home.html')
    
    cart_total = Cart_total.objects.get(user = request.user)
    total_pay = cart_total.total_amount
    address = Addresses.objects.get(id = request.session['address_id'])

    if 'COD' in request.GET:
        new_order = Order.objects.create(user = request.user,order_total=total_pay,order_status='Booked', order_address=address.address)
        new_order.save()
        print()

        for cart_item in cart_items:
            order_item = Order_items.objects.create(order_id=new_order, product=cart_item.product, product_quantity=cart_item.quantity,  product_price=cart_item.product.product_price)
            order_item.save()
            cart_item.product.product_quantity =  cart_item.product.product_quantity - cart_item.quantity
            cart_item.save()

        cart_items.delete()
        total_amount_obj = Cart_total.objects.get(user = request.user)
        print('total---------------------------------------------before',total_amount_obj.total_amount)
        total_amount_obj.total_amount = 0
        total_amount_obj.save()
        print('total---------------------------------------------after',total_amount_obj.total_amount)
        return render(request,'save_success.html')
    
    if "ONLINE_PAYMENT" in request.GET:

        new_order = Order.objects.create(user = request.user,order_total=total_pay, order_status='Booked', order_address=address.address,payment_order_id=request.GET['razor_payment_id'], razorpay_order_id=request.GET['razor_order_id'])
        new_order.save()
        print()

        for cart_item in cart_items:
            order_item = Order_items.objects.create(order_id=new_order, product=cart_item.product, product_quantity=cart_item.quantity,  product_price=cart_item.product.product_price)
            order_item.save()
            cart_item.product.product_quantity =  cart_item.product.product_quantity - cart_item.quantity
            cart_item.save()

        cart_items.delete()
        total_amount_obj = Cart_total.objects.get(user = request.user)
        print('total---------------------------------------------before',total_amount_obj.total_amount)
        total_amount_obj.total_amount = 0
        total_amount_obj.save()
        print('total---------------------------------------------after',total_amount_obj.total_amount)
        return render(request,'save_success.html')
     
    return render(request,'place_order.html',{'address':address,'cart_items': cart_items,'api_key':settings.RAZORPAY_API_KEY,'total_amount':total_pay})


def razor_order(request):

    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))
    DATA = {
        "amount": 1000,
        "currency": "INR",
        "receipt": "receipt#1"
    }
    payment_order = client.order.create(data=DATA)
    payment_order_id = payment_order['id']
    print('sdfsdfsd-----------------------------------',payment_order['id'])
    return JsonResponse({'payment_order_id':payment_order_id,'api_key':settings.RAZORPAY_API_KEY})
    
    



            
    #         client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))
    #         DATA = {
    #             "amount": 500,
    #             "currency": "INR",
    #             "receipt": "receipt#1"
    #         }
    #         payment_order = client.order.create(data=DATA)
    #         payment_order_id = payment_order['id']
    #         print('sdfsdfsd-----------------------------------',payment_order['id'])
    #         return render(request,'place_order.html',{'address':address,'cart_items': cart_items,'payment_order_id':payment_order_id,'api_key':settings.RAZORPAY_API_KEY,'total_amount':total_pay})
        

        
    #     print('asdasdasdasaaaaaaaaaaaaaaa-----------------------------------------------',cart_items)
    #     client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))
    #     DATA = {
    #         "amount": 5000,
    #         "currency": "INR",
    #     }
    #     payment_order= client.order.create(data=DATA)
    #     payment_order_id = payment_order['id']
    #     return render(request,'place_order.html',{'address':new_address,'cart_items': cart_items,'payment_order_id':payment_order_id,'api_key':settings.RAZORPAY_API_KEY,'total_amount':total_pay})
    # print('entered into create order')

    # address = Addresses.objects.get(id = request.GET['address_id'])
    # cart_items = Cart.objects.filter(user = request.user)
    # print('cart tiem exits or nor---------------------------',cart_items)

    # if cart_items.exists() == False:
    #     return render(request,'home.html')

    # if 'COD' in request.GET:


    # for key,value in request.GET.items():
    #     print('key is:',key, 'the value is :', value )

    # new_order = Order.objects.create(user = request.user,order_total=request.GET['total_amount'],order_status='Booked', payment_order_id=request.GET['razor_payment_id'], order_address=address.address, razorpay_order_id=request.GET['razor_order_id'])
    # new_order.save()


    # for cart_item in cart_items:
    #     order_item = Order_items.objects.create(order_id=new_order, product=cart_item.product, product_quantity=cart_item.quantity,  product_price=cart_item.product.product_price)
    #     order_item.save()
    #     cart_item.product.product_quantity =  cart_item.product.product_quantity - cart_item.quantity 
    #     cart_item.save()

    # cart_items.delete()
    # total_amount_obj = Cart_total.objects.get(user = request.user)
    # print('total---------------------------------------------before',total_amount_obj.total_amount)
    # total_amount_obj.total_amount = 0
    # total_amount_obj.save()
    # print('total---------------------------------------------after',total_amount_obj.total_amount)
    # return JsonResponse({'message':'success'})