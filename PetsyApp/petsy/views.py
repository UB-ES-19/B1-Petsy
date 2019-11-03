from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout

from petsy.forms import *
from petsy.models import *
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import ast
import time

#Petsy
def index(request):

    if request.user.is_authenticated:
        user = UserPetsy.objects.all().get(email=request.user.email)
        context = {
            "user": user
        }
        return render(request, 'petsy/homepage.html', context)

    return render(request, 'petsy/homepage.html')

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
                user = UserPetsy.objects.create_user(username=username, email=email, password=password)
                user.save()

                shop_user = Shop(
                    shop_name="Shop",
                    user_owner=user
                )
                shop_user.save()

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


@login_required
def create(request):
    context = {
        'dict_cat': Product._d_categories,
        'product_form': ProductForm()
    }
    return render(request, 'petsy/createProduct.html', context)


"""
# Vista de productos (testing)
def products(request, username=None):
    print("REQUEST: ", request)
    if username:
        response = "You are looking for %s's products" % username
    else:
        response = "You are looking for featured products"
    return HttpResponse(response)

"""
@login_required
def profile(request, id_user=None):

    user = UserPetsy.objects.all().get(id_user=id_user)
    products = list(Product.objects.all())
    shops = Shop.objects.all().filter(user_owner=user)
    context = {
        "user": user,
        "list_products": products,
        "shop_list": shops
    }
    return render(request, 'petsy/profile.html', context)
    #return HttpResponseRedirect('profile/', context)


def shop(request, id_shop=None):

    _shop = Shop.objects.all().get(id_shop=id_shop)
    product_list = list(Product.objects.all().filter(shop=_shop))
    context = {
        "shop": _shop,
        "list_products": product_list
    }
    #return HttpResponseRedirect('', context)
    return render(request, 'petsy/shop.html', context)

#ProductManagerApp
def get_product_by_id(request, id_product=None):
    """
    :param request:
    :param id_product:
    :return:
    """

    if request.method == 'GET':
        product_id = id_product if id_product is not None else request.GET['product_id']

        try:
            product = Product.objects.get(idProduct=product_id)
        except:
            return JsonResponse({
                "response_msg": "Error: El producto no existe",
                "response_code": 404  # Product not found
            })

        return render(request, 'petsy/product.html', {
            "product": product
        })

def get_user(request):
    """

    :param request:
    :return: {
                "user": ESdinou,
                "photo": photo.png
                "description": hola soc ESdinou
                "follower_count:
    """
    shop = Shop.objects.get(user_owner=request.user)
    products = Product.objects.get(id_shop=shop.id_shop)
    print(products)
    product_array = []
    for i in range(4):
        product_array.append(products[i])

    return render(request, 'petsy/profile.html.html', {
        "user": request.POST['username'],
        "photo": request.POST['photo'],
        "description": request.POST['description'],
        "follower_count": request.POST['follower_count'],
        "following_users": request.POST['following_users'],
        "favorite_products": request.POST['favorite_products'],
        "shop_name": shop.shop_name,
        "id_shop": shop.id_shop,
        "products_array": product_array
    })


def review_product_by_id(request):
    """
    That function expects a request with the following body:
        {
            "product_id": 4,
            "review": "Very good quality, I really recommend it bc...",
            "rate": 3,
            "username": "joseluis"
        }
    And then, updates the field 'reviews' from the 'product_id' product.

    :param request
    :return: JsonResponse
    """
    id_product = request.POST['product_id']
    product_to_update = Product.objects.get(idProduct=id_product)
    new_review = request.POST['review']
    new_rate = request.POST['rate']
    user = request.user.username  # "joseluis"  # request.POST['username']

    actual_reviews = product_to_update.reviews
    review_array = ast.literal_eval(actual_reviews)

    new_review_obj = {
        "user": {
            "profile_pic": "default_user.png",
            "username": user
        },
        "date": time.strftime('%y/%m/%d %X'),
        "message": new_review
    }

    review_array.append(new_review_obj)

    updated_sum_votes = product_to_update.sum_votes + float(new_rate)
    updated_num_votes = product_to_update.num_votes + 1

    Product.objects. \
        filter(idProduct=id_product). \
        update(sum_votes=updated_sum_votes, num_votes=updated_num_votes, reviews=str(review_array))

    product = Product.objects.get(idProduct=id_product)

    # return HttpResponseRedirect('id/'+str(id_product), {
    #     "titulo": product.nameProduct,
    #     "descripcion": product.description,
    #     "categoria": product.category,
    #     "precio": product.price,
    #     "materiales": product.materials,
    #     "img": product.featured_photo,
    #     "num_votes": product.num_votes,
    #     "sum_votes": product.sum_votes,
    #     "shop_id": product.id_shop,
    #     "reviews": ast.literal_eval(product.reviews)
    # })
    #
    return render(request, 'petsy/product.html', {
        "titulo": product.nameProduct,
        "descripcion": product.description,
        "categoria": product.category,
        "precio": product.price,
        "materiales": product.materials,
        "img": product.featured_photo,
        "num_votes": product.num_votes,
        "sum_votes": product.sum_votes,
        "shop_id": product.id_shop,
        "reviews": ast.literal_eval(product.reviews),
        "id_product": product.idProduct
    })


def remove_product(request, id_product=None):
    """
    :param request:
    :param id_product:
    :return:
    """
    if request.method == 'GET':
        product_id = id_product if id_product is not None else request.GET['product_id']

        try:
            product = Product.objects.get(idProduct=product_id)
            product.remove()

        except:
            return JsonResponse({
                "response_msg": "Error: El producto no existe",
                "response_code": 404  # Product not found
            })

        return JsonResponse({
            "result_code": 200
        })


def create_product(request):
    """
    Register a new user into database

    :param request: Request
    :return: ????????
    """
    if request.method == 'POST':

        username = request.user
        user = User.objects.get(username=username)
        """
        try:
            shop = Shop.objects.get(user_owner=user).id_shop
            print("Shop already exists.")
        except:
            print("No shop yet, creating a new one.")
            shop = Shop(
                shop_name="Shop",
                user_owner=user
            )
            shop.save()
        """

        shop = Shop.objects.get(user_owner=user)
        product = ProductForm(request.POST, request.FILES)
        if product.is_valid():
            p = product.save(commit=False)
            p.shop = shop
            p.save()
            return HttpResponseRedirect(str(p.idProduct))
    return HttpResponse('')

