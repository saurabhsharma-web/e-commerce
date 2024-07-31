from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from .models import Product,Customer,Cart,OrderPlace,Payment,Wishlist
from .forms import CustomerForm
from django.contrib import messages
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.db.models import Q
import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.
@login_required
def home(request):
    totalitems = 0
    if request.user.is_authenticated:
        totalitems =len(Cart.objects.filter(user=request.user))
    return render(request,'app/index.html',locals())
@login_required
def about(request):
    totalitems = 0
    if request.user.is_authenticated:
        totalitems =len(Cart.objects.filter(user=request.user))
    return render(request,'app/about.html',locals())
@login_required
def contect(request):
    totalitems = 0
    if request.user.is_authenticated:
        totalitems =len(Cart.objects.filter(user=request.user))
        
    return render(request,'app/contect.html',locals())

def ragistration(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        context={}
        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="Fields can not be empty"
            return render(request,'app/registration.html',context)
        elif upass != ucpass:
            context['errmsg']="password & confirm password didn't matched"
            return render(request,'app/registration.html',context)
        else:
            try:
                u=User.objects.create(password=upass,username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context['success']="User Created successfully,Please Login"
                return render(request,'app/registration.html',context)
                #return HttpResponse("user create successfully")
            except Exception:
                context['errmsg']="User is already existe"
                return render(request,'app/registration.html',context)
       
    else:

        return render(request,'app/registration.html')

@login_required
def user_login(request):
    if  request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        #print(uname,"--",upass)
        #return HttpResponse("Data is fetched")
        context={}
        if uname=="" or upass=="":
            context['errmsg']="Field can not be empaty"
            return render(request,'app/login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            #print(u) #if is it correct then give objects,none
            #print(u.username)
            #print(u.is_superuser)
            #return HttpResponse("in else part ")
            if u is not None:
                login(request,u) # start session
                return redirect('/')
            else:
                context['errmsg']="Invailid username and password"
                return render(request,'app/login.html',context)
    else:
        return render(request,'app/login.html')

@method_decorator(login_required,name='dispatch')
class profile(View):
    def get(self,request):
        form = CustomerForm()
        totalitems = 0
        if request.user.is_authenticated:
            totalitems =len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', locals())

    def post(self,request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request, 'Profile updated successfully.')  
        else:
            messages.error(request, 'Profile update failed.')
        return render(request, 'app/profile.html', locals())




@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitems = 0
    if request.user.is_authenticated:
        totalitems =len(Cart.objects.filter(user=request.user))
    return render(request, 'app/address.html', locals())


@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerForm(instance=add) # what ever data(pk) is return that data automatic added
        totalitems = 0
        if request.user.is_authenticated:
            totalitems =len(Cart.objects.filter(user=request.user))
        return render(request, 'app/updateaddress.html', locals())

    def post(self,request,pk):
        form = CustomerForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request, 'Profile updated successfully.')  
        else:
            messages.error(request, 'Profile update failed.')
        return redirect('address')


def user_logout(request):
    logout(request)
    return redirect('/')

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')  # get is a method we get the product id help of this urls
    product = Product.objects.get(id=product_id) # helf of above id we get th object id (product id)
    Cart(user=user,product=product).save() #by defaut qty is 1
    return redirect('/cart')

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.descount_price
        amount = amount + value
    totalamount = amount + 40 # shipping charges
    totalitems = 0
    if request.user.is_authenticated:
        totalitems =len(Cart.objects.filter(user=request.user))
    return render(request,'app/addtocart.html',locals())

@login_required
def checkout(request):
    totalitems = 0
    if request.user.is_authenticated:
        totalitems =len(Cart.objects.filter(user=request.user))
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    famount = 0
    for p in cart_items:
        value = p.quantity * p.product.descount_price
        famount = famount + value
        totalamount = famount + 40 
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET)) #it is object of client
        data = {"amount":razoramount, "currency":"INR"} # i create dict for pass dynamick values
        payment_response = client.order.create(data=data) # client is method views
        print(payment_response)
        #{'amount': 8500, 'amount_due': 8500, 'amount_paid': 0, 'attempts': 0, 'created_at': 1721995946, 'currency': 'INR', 'entity': 'order', 'id': 'order_OdFxWEPhSzHuof', 'notes': [], 'offer_id': None, 'receipt': None, 'status': 'created'}
        #{'amount': 20500, 'amount_due': 20500, 'amount_paid': 0, 'attempts': 0, 'created_at': 1721995946, 'currency': 'INR', 'entity': 'order', 'id': 'order_OdFxWi5kIl9Vu3', 'notes': [], 'offer_id': None, 'receipt': None, 'status': 'created'}  
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment=Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_Payment_status = order_status
            )
            payment.save()
    return render(request,'app/checkout.html',locals())

@login_required
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    #print("payment_done:oid = " , order_id,pid = ",payment_id,"cid=", cust_id)
    user=request.user
    #return redirect("orders")
    customer=Customer.objects.get(id=cust_id)
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    # to save order details
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlace(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.delete()
    return redirect('orders')


@login_required
def orders(request):
    totalitems = 0
    if request.user.is_authenticated:
        totalitems =len(Cart.objects.filter(user=request.user))
    order_placed = OrderPlace.objects.filter(user=request.user)
    print(order_placed[0])
    return render(request,'app/orders.html',locals())

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))
        c.quantity = c.quantity + 1 # to increase the qty and save in cart
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.descount_price
            amount = amount + value
        totalamount = amount + 40 # shipping charges
        #print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount,
            
        }
        return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))
        if c.quantity > 1: # to prevent from decreasing qty to zero or less than zero
            c.quantity = c.quantity - 1 # to increase the qty and save in cart
            c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.descount_price
            amount = amount + value
        totalamount = amount + 40 # shipping charges
        #print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount,
            
        }
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))
        c.quantity = c.quantity + 1 # to increase the qty and save in cart
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.descount_price
            amount = amount + value
        totalamount = amount + 40 # shipping charges
        #print(prod_id)
        data={
            'amount':amount,
            'totalamount':totalamount,
            
        }
        return JsonResponse(data)


@login_required
def cat(request,val):
    totalitems = 0
    if request.user.is_authenticated:
        totalitems =len(Cart.objects.filter(user=request.user))
    product = Product.objects.filter(category=val)
    title = Product.objects.filter(category=val).values('title')
    
    return render (request,'app/category.html',locals())



def categorytitle(request,val):
    product = Product.objects.filter(title=val)
    title = Product.objects.filter(category=product[0].category).values('title')  #we get the all titles of that cotegory product 
    totalitems = 0
    if request.user.is_authenticated:
        totalitems =len(Cart.objects.filter(user=request.user))
    return render (request,'app/category.html',locals())


def productdetails(request,pk):
    product = Product.objects.get(id=pk)
    wishlist =Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
    print(wishlist)

    totalitems = 0
    if request.user.is_authenticated:
        totalitems =len(Cart.objects.filter(user=request.user))
    return render (request,'app/product_details.html',locals())

def search_products(request):
    query = request.GET['query']
    print(f"query : {query}")
    totalitems = 0
    if request.user.is_authenticated:
        totalitems =len(Cart.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query))
    
    return render(request,'app/search.html',locals())