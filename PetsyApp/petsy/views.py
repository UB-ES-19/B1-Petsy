from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
# User registration stuff
from django.contrib.auth import login, authenticate
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

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
    return redirect('index')


def login_user(request):
    """
    This method checks whether the combination user/password exists or not

    :param request: Request
    :return: User if connected, None otherwise
    """
    if request.method == 'POST':
        username = request.POST["email_login"]
        password = request.POST["password_login"]
        #go_to_url = request.POST["redirect_url"] or "/"

        print(username)
        print(password)

        user = authenticate(email=username, password=password)

        if user is not None:
            login(request, user)
            print("patata")

        return render(request, 'petsy/index.html')


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
