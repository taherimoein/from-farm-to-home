from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json,datetime
# get model
from main.models import User,Product,Order,OrderDetails

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def indexpage(request):
    return render(request,'index.html')


def signin_page(request):
    if not request.user.is_authenticated: 
        return render(request, 'main/account/signin.html')
    else:
        return redirect('main:indexpage')


def signout(request):
    if request.user.is_authenticated: 
        logout(request)
        return redirect('main:indexpage')
    else:
        return redirect('main:indexpage')


@csrf_exempt
@require_http_methods(['POST'])
def signin(request):
    response_data = {}
    try:
        email = request.POST.get('email')
        password = request.POST.get('password')
        # get this user
        user = authenticate(request,username=email,password=password)
        # check user
        if user is not None:
            # login user
            login(request, user)

            response_data['status'] = '200'
            return JsonResponse(response_data)
        else:
            response_data['status'] = '404'
            return JsonResponse(response_data)
    except Exception as e:
        response_data['status'] = '500'
        return JsonResponse(response_data)


@csrf_exempt
def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    elif request.method == 'POST':
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            address = request.POST.get('address')
            zipcode = request.POST.get('zipcode')
            if not User.objects.filter(email=email).exists():
                # create user
                user = User.objects.create(first_name=first_name,last_name=last_name,email=email,address=address,zipcode=zipcode)
                user.set_password(password)
                # login user
                login(request, user)

                return redirect('main:indexpage')
            else:
                return redirect('main:register')
        except Exception as e:
            return redirect('main:register')


@csrf_exempt
def products(request):
    if request.method == 'GET':
        # get products
        products = Product.objects.all()

        context = {
            'Products': products
        }
        return render(request,'products.html',context)
    elif request.method == 'POST':
        # get search
        search = request.POST.get('terms')
        # set search regex
        search = search.split(' ')
        search = list(filter(lambda i: i != '', search))
        search_word_list = []
        for word in search:
            search_word = list(map(lambda x: x + '\s*', word.replace(' ','')[:-1]))
            search_word = ''.join(search_word) + word[-1]
            search_word_list.append(search_word)
        search_word = r'.*'.join(search_word_list)
        # search in fullname & nationalcode
        products = Product.objects.filter(title__regex = search_word)

        context = {
            'Products': products
        }
        return render(request,'products.html',context)


def product_page(request,pk):
    # get product
    productObj = get_object_or_404(Product,id=pk)

    context = {
        'Product': productObj
    }
    return render(request,'product_page.html',context)


def account(request):
    # get user
    userObj = request.user
    # get orders
    orders = userObj.order_user.all()

    context = {
        'User': userObj,
        'Orders': orders
    }
    return render(request,'account.html',context)


@csrf_exempt
def cart(request):
    if request.method == 'GET':
        # get order
        if Order.objects.filter(user=request.user,status=False).exists():
            OrderObj = Order.objects.get(user=request.user,status=False)

            context = {
                'OrderObj': OrderObj
            }
            return render(request,'cart.html',context)
        else:
            return render(request,'index.html')
    elif request.method == 'POST':
        response_data = {}
        # get product
        product_id = request.POST.get('id')
        productObj = Product.objects.get(id=product_id)

        userObj = request.user
        if not Order.objects.filter(user=userObj,status=False).exists():
            OrderObj = Order.objects.create(user=userObj,email=userObj.email,address=userObj.address,zipcode=userObj.zipcode)
        else:
            OrderObj = Order.objects.get(user=userObj,status=False)
        # add items
        if OrderObj.items.filter(product=productObj).exists():
            OrderDetailsObj = OrderObj.items.get(product=productObj)
            OrderDetailsObj.count += 1
            OrderDetailsObj.save()
        else:
            OrderDetailsObj = OrderDetails.objects.create(product=productObj,price=productObj.price,count=1)
            OrderObj.items.add(OrderDetailsObj)

        totalPrice = 0
        for item in OrderObj.items.all():
            totalPrice += item.price
        OrderObj.total_price = totalPrice
        OrderObj.save()

        response_data['status'] = '200'
        return JsonResponse(response_data)


@csrf_exempt
def checkout(request):
    if request.method == 'GET':
        return render(request,'success.html')
    elif request.method == 'POST':
        response_data = {}
        payment_type = request.POST.get('payment_type')

        userObj = request.user
        if Order.objects.filter(user=userObj,status=False).exists():
            OrderObj = Order.objects.get(user=userObj,status=False)
            OrderObj.payment_type = payment_type
            OrderObj.status = True
            OrderObj.save()

        response_data['status'] = '200'
        return JsonResponse(response_data)