from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
# User registration stuff
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm


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
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_user(request):
    """
    This method checks whether the combination user/password exists or not

    :param request: Request
    :return: User if connected, None otherwise
    """
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return ""


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
