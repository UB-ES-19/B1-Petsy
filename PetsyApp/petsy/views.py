from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
# User registration stuff
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, reverse

from django.views.generic.edit import CreateView

from django.urls import reverse_lazy
#from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django.contrib.auth.models import User


def index(request):
    return render(request, 'petsy/index.html')


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
        form = SignUpForm()
        username = (request.POST['username'])
        email = (request.POST['email'])
        password = (request.POST['password'])

        try:
            users = User.objects.get(username=username)
        except:
            user = User.objects.create_user(username=username, email=email, password=password)

        print("\n******************************")
        print(user)
        print("******************************\n")

        user.save()
    return render(request, 'petsy/index.html')


def login_user(request):
    """
    This method checks whether the combination user/password exists or not

    :param request: Request
    :return: User if connected, None otherwise
    """
    if request.method == 'POST':
        mail = request.POST["email_login"]
        password = request.POST["password_login"]
        go_to_url = "petsy/index.html"  # request.POST["redirect_url"] or "petsy/index.html"

        print(mail)
        print(password)

        try:
            username = User.objects.get(email=mail).username
        except:
            return render(request, go_to_url)
            #return HttpResponseRedirect('/')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            print(user, " has logged in.")
        else:
            print("User is None :/")

        return HttpResponseRedirect('/')


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
