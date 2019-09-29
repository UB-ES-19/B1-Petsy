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
    if username:
        response = "You are looking for %s's products" % username
    else:
        response = "You are looking for featured products"
    return HttpResponse(response)


# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             new_user = form.save()
#             login(request, new_user)
#             return HttpResponseRedirect(reverse("index"))
#         else:
#             form = UserCreationForm()
#         return render(request, "registration/register.html", {
#             'form': form
#         })


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'index.html', {'form': form})