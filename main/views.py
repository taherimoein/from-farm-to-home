from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
# get model
from main.models import User

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

            return redirect('main:indexpage')
        else:
            return redirect('main:indexpage')
    except Exception as e:
        return redirect('main:indexpage')


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