from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
# User registration stuff
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, reverse

from django.views.generic.edit import CreateView

from django.urls import reverse_lazy
# from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django.contrib.auth.models import User


def index(request):
    return render(request, 'petsy/homepage.html')


# Vista de productos (testing)
def products(request, username=None):
    print("REQUEST: ", request)
    if username:
        response = "You are looking for %s's products" % username
    else:
        response = "You are looking for featured products"
    return HttpResponse(response)


def signup(request):
    """
    Register a new user into database

    :param request: Request
    :return: ????????
    """
    if request.method == 'POST':
        username = (request.POST['username'])
        email = (request.POST['email'])
        password = (request.POST['password'])

        try:
            user = User.objects.get(username=username)
            return JsonResponse({
                'signup_successful': False,
                'response_code': 403  # That username already exists
            })
        except:
            try:
                user = User.objects.get(email=email)
                return JsonResponse({
                    'signup_successful': False,
                    'response_code': 402  # That email already exists
                })
            except:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return JsonResponse({
                    'signup_successful': True,
                    'response_code': 200  # That username already exists
                })


def login_user(request):
    """
    This method checks whether the combination user/password exists or not

    :param request: Request
    :return: User if connected, None otherwise
    """

    if request.method == 'POST':
        mail = request.POST["email_login"]
        password = request.POST["password_login"]

        # print(mail)
        # print(password)

        try:
            username = User.objects.get(email=mail).username
        except:
            return JsonResponse({
                'login_successful': False,
                'response_code': 404  # Username with that email does not exists
            })

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            print(user, " has logged in.")
            return JsonResponse({
                'login_successful': True,
                'response_code': 200
            })
        else:
            print("User is None :/")
            return JsonResponse({
                'login_successful': False,
                'response_code': 403  # Wrong password
            })


def _check_user_connected(request):
    """
    Returns the User connected

    :param request: Request
    :return: User connected or None
    """
    if request.user.is_authenticated():
        return request.user
    else:
        return None


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def create(request):
    return render(request, 'petsy/create-product.html')
