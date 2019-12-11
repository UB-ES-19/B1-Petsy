from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout

from petsy.forms import *
from petsy.models import *
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from itertools import chain
import ast
import time


# Petsy

class SearchProductView(ListView):
    model = Product
    template_name = 'petsy/show_products.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        list_items = Product.objects.filter(nameProduct__icontains=query)

        return list_items


class SearchShopView(ListView):
    model = Shop
    template_name = 'petsy/show_products.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        list_items = Shop.objects.filter(shop_name__icontains=query)

        return list_items


class SearchUserView(ListView):
    model = User
    template_name = 'petsy/show_products.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        list_items = User.objects.filter(username__icontains=query)

        return list_items


def index(request):
    if request.user.is_authenticated:
        user = UserPetsy.objects.all().get(email=request.user.email)
        shops = Shop.objects.all().filter(user_owner=user)
        context = {
            "user": user,
            "list_shops": shops
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
def create(request, id_shop=None):
    user = UserPetsy.objects.all().get(email=request.user.email)
    shops = Shop.objects.all().filter(user_owner=user)
    context = {
        'user': user,
        'dict_cat': Product._d_categories,
        'product_form': ProductForm(),
        'list_shops': shops,
        'id_shop_actual': id_shop
    }
    return render(request, 'petsy/createProduct.html', context)

@login_required
def create_shop_view(request):
    user = UserPetsy.objects.all().get(email=request.user.email)
    shops = Shop.objects.all().filter(user_owner=user)
    context = {
        'user': user,
        'shop_form': ShopForm(),
        'list_shops': shops,
    }
    return render(request, 'petsy/createShop.html', context)
@login_required
def edit_shop_view(request, id_shop=None):
    user = UserPetsy.objects.all().get(email=request.user.email)
    shops = Shop.objects.all().filter(user_owner=user)
    _shop = Shop.objects.all().get(id_shop=id_shop)
    context = {
        'user': user,
        'shop_form': EditForm(instance=_shop),
        'list_shops': shops,
        'shop': _shop
    }
    return render(request, 'petsy/editShop.html', context)
@login_required
def edit_product(request, id=None):
    if request.method == "GET":
        print(id)
        user = UserPetsy.objects.all().get(email=request.user.email)
        shops = Shop.objects.all().filter(user_owner=user)
        product = Product.objects.all().get(idProduct=int(id))
        form = ProductForm(instance=product)
        #form.img = product.img.url
        context = {
            'product': product,
            'user': user,
            'dict_cat': Product._d_categories,
            'product_form': form,
            'list_shops': shops
        }
        return render(request, 'petsy/editProduct.html', context)

@login_required
def edit_profile(request):
    if request.method == "POST":
        user = UserPetsy.objects.all().get(id=request.user.id)

        #patata = False
        #patata2 = False
        if request.POST["username"] != "":
            user.username = request.POST["username"]
            #patata = True
        if len(request.FILES) != 0:
            user.photo = request.FILES["photo"]
            #patata2 = True

        user.save()
        return redirect(profile, user.id)


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


def profile(request, id=None):
    user = UserPetsy.objects.all().get(id=id)
    shops = Shop.objects.all().filter(user_owner=user)
    _shops = Shop.objects.all().filter(user_owner=request.user)
    followers = user.follower.all().count()
    following = user.following.all().count()
    fav_shops = user.shop_faved.all()
    products = user.prod_faved.all()

    """
    product_list = []
    for shop in shops:
        product_list.append(Product.objects.all().filter(shop=shop.id_shop))
    """

    if request.user.is_authenticated:

        if request.user.id == int(id):
            yo = UserPetsy.objects.all().get(id=request.user.id)
            context = {
                "user": user,
                "followers": followers,
                "following": following,
                "shops": shops,
                "list_shops": _shops,
                "list_items": fav_shops,
                "follow": yo.following.filter(following=user).count() == 1,
                "list_products": products,
                "edit_form": EditProfileForm(instance=user)

            }
        else:

            yo = UserPetsy.objects.all().get(id=request.user.id)
            context = {
                "user": user,
                "followers": followers,
                "following": following,
                "shops": shops,
                "list_shops": _shops,
                "list_items": fav_shops,
                "follow": yo.following.filter(following=user).count() == 1,
                "list_products": products
            }
    else:
        context = {
            "user": user,
            "followers": followers,
            "following": following,
            "list_shops": shops,
            "list_items": fav_shops,
            "follow": False,
            "list_products": products
        }
    return render(request, 'petsy/profile.html', context)


def shop(request, id_shop=None):
    _shop = Shop.objects.all().get(id_shop=id_shop)
    product_list = list(Product.objects.all().filter(shop=_shop))
    user = UserPetsy.objects.all().get(email=_shop.user_owner.email)
    shops = Shop.objects.all().filter(user_owner=request.user)

    if request.user.is_authenticated:
        yo = UserPetsy.objects.all().get(id=request.user.id)
        context = {
            "shop": _shop,
            "list_products": product_list,
            "user": user,
            "favorited": yo.shop_faved.filter(shop_faved=_shop).count() == 1,
            "list_shops": shops
        }
    else:
        context = {
            "shop": _shop,
            "list_products": product_list,
            "user": user
        }
    return render(request, 'petsy/shop.html', context)


def get_product_by_id(request, id_product=None):
    """
    :param request:
    :param id_product:
    :return:
    """

    if request.method == 'GET':
        product_id = id_product if id_product is not None else request.GET['product_id']
        user = UserPetsy.objects.all().get(email=request.user.email)
        _shops = Shop.objects.all().filter(user_owner=request.user)
        ownership = False

        try:
            product = Product.objects.get(idProduct=product_id)

        except:
            return JsonResponse({
                "response_msg": "Error: El producto no existe",
                "response_code": 404  # Product not found
            })

        if request.user.is_authenticated and request.user.id == product.shop.user_owner.id:
            ownership = True

        return render(request, 'petsy/product.html', {
            "product": product,
            "reviews": ast.literal_eval(product.reviews),
            "list_shops": _shops,
            "favorited": user.prod_faved.filter(prod_faved=product).count() == 1,
            "owner": ownership
        })

def get_shop_by_id(request, id_shop=None):
    """
    :param request:
    :param id_product:
    :return:
    """

    if request.method == 'GET':
        shop_id = id_shop if id_shop is not None else request.GET['shop_id']
        user = UserPetsy.objects.all().get(email=request.user.email)
        _shops = Shop.objects.all().filter(user_owner=request.user)

        try:
            s = Shop.objects.get(id_shop=shop_id)

        except:
            return JsonResponse({
                "response_msg": "Error: la tienda no existe",
                "response_code": 404  # Product not found
            })

        return render(request, 'petsy/shop.html', {
            "shop": s,
            "list_shops": _shops
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
    #print(products)
    product_array = []
    for i in range(4):
        product_array.append(products[i])

    return render(request, 'petsy/profile.html', {
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



@login_required()
def following_users(request):
    if request.method == 'POST':
        follower = get_object_or_404(UserPetsy, id=request.user.id)
        following = get_object_or_404(UserPetsy, id=request.POST['following'])

        relation = follower.following.filter(following=following)
        if relation:
            relation.delete()
            return JsonResponse({
                "response_msg": "Dejar de seguir OK!",
                "response_code": 200
            })
        else:
            follower.following.add(UserFollowing(following=following), bulk=False)
            return JsonResponse({
                "response_msg": "Seguir usuario OK!",
                "response_code": 201
            })

    return JsonResponse({
        "response_msg": "Error: GET encontrado",
        "response_code": 400
    })


@login_required()
def favorite_shop(request):
    if request.method == 'POST':
        # print(request.POST['shop_favorited'])
        follower = get_object_or_404(UserPetsy, id=request.user.id)
        shop_favorited = get_object_or_404(Shop, id_shop=request.POST['following'])

        relation = follower.shop_faved.filter(shop_faved=shop_favorited)
        if relation:
            relation.delete()
            return JsonResponse({
                "response_msg": "Dejar de seguir tienda OK!",
                "response_code": 200
            })
        else:
            follower.shop_faved.add(ShopFavorited(shop_faved=shop_favorited), bulk=False)
            return JsonResponse({
                "response_msg": "Seguir tienda OK!",
                "response_code": 201
            })

    return JsonResponse({
        "response_msg": "Error: GET encontrado",
        "response_code": 400
    })

@login_required()
def favorite_product(request):
    if request.method == "POST":
        follower = get_object_or_404(UserPetsy, id=request.user.id)
        prod_favorited = get_object_or_404(Product, idProduct=request.POST['following'])

        relation = follower.prod_faved.filter(prod_faved=prod_favorited)

        if relation:
            relation.delete()
            return JsonResponse({
                "response_msg": "Objeto quitado de favoritos",
                "response_code": 200
            })
        else:
            follower.prod_faved.add(ProductFavorited(prod_faved=prod_favorited), bulk=False)
            return JsonResponse({
                "response_msg": "Objeto añadido a favoritos",
                "response_code": 201
            })
    return JsonResponse({
        "response_msg": "GET encontrado",
        "response_code": 400
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
    id = request.user.id

    actual_reviews = product_to_update.reviews
    review_array = ast.literal_eval(actual_reviews)

    new_review_obj = {
        "user": {
            "profile_pic": "default_user.png",
            "username": user,
            "id": id
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

    return redirect(get_product_by_id, id_product=product.idProduct)


def show_profile_followers(request, id=None, type="follower"):
    user = UserPetsy.objects.all().get(id=id)
    if type == "following":
        list_users = user.following.filter(follower=user)
        aux = [user.following for user in list_users]

    else:
        list_users = user.follower.filter(following=user)
        aux = [user.follower for user in list_users]

    context = {
        "type": "user",
        "list_items": aux,
    }
    return render(request, 'petsy/show_products.html', context)


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


def create_product(request,id_shop=None):
    """
    Register a new user into database

    :param request: Request
    :return: ????????
    """
    if request.method == 'POST':

        username = request.user
        user = UserPetsy.objects.get(username=username)


        try:
            shop = Shop.objects.get(id_shop=id_shop)
            print("Shop already exists.")
        except:
            print("No shop yet, creating a new one.")
            shop = Shop(
                shop_name="Shop",
                user_owner=user
            )
            shop.save()


        product = ProductForm(request.POST, request.FILES)
        if product.is_valid():
            p = product.save(commit=False)
            p.shop = shop
            p.save()
            return redirect(get_product_by_id, id_product=p.idProduct)
    return HttpResponse('')

def create_shop(request):
    """
    Register a new user into database

    :param request: Request
    :return: ????????
    """
    if request.method == 'POST':

        username = request.user
        user = UserPetsy.objects.get(username=username)


        """try:
            shop = Shop.objects.get(user_owner=user).id_shop
            print("Shop already exists.")
        except:
            print("No shop yet, creating a new one.")
            shop = Shop(
                shop_name="Shop",
                user_owner=user
        )"""

        shop = ShopForm(request.POST, request.FILES)
        if shop.is_valid():
            s = shop.save(commit=False)
            s.user_owner = user
            shop.save()
            return redirect(get_shop_by_id, id_shop=s.id_shop)
    return HttpResponse('')

def edit_shop(request, id_shop=None):
    if request.method == "POST":
        shop = Shop.objects.get(id_shop=id_shop)

        if request.POST["shop_name"] != "":
            shop.shop_name = request.POST["shop_name"]

        if len(request.FILES) != 0:
            shop.img_shop = request.FILES["img_shop"]

        if request.POST["description"] != "":
            shop.description = request.POST["description"]



        shop.save()

        return redirect(get_shop_by_id, id_shop=shop.id_shop)
@login_required()
def edit_product_data(request, id=None):
    if request.method == "POST":
        user = UserPetsy.objects.all().get(id=request.user.id)
        product = Product.objects.all().get(idProduct=id)
        edited = ProductForm(request.POST, request.FILES)

        if edited.is_valid():
            edited = edited.save(commit=False)
            product.nameProduct = edited.nameProduct
            product.description = edited.description
            product.category = edited.category
            product.price = edited.price
            if len(request.FILES) > 0:
                product.img = edited.img
            product.materials = edited.materials
            product.save()

        return redirect(get_product_by_id, id_product=product.idProduct)


def searching(object, search, edit_distance):
    from .levenshtein import levenshtein_func

    if (object == 'product'):
        result = list(set(Product.objects.values_list('result', flat=True)))

    elif (object == 'username'):
        result = list(set(UserPetsy.objects.values_list('result', flat=True)))

    elif (object == 'shop'):
        result = list(set(Shop.objects.values_list('result', flat=True)))

    search_dist = [(x, levenshtein_func(x.lower(), search.lower())) for x in result if
                   levenshtein_func(x.lower(), search.lower()) <= edit_distance]
    search_dist += [(x, len(x) - len(search)) for x in result if search.lower() in x.lower()]
    search_dist.sort(key=lambda x: x[1])
    if len(search_dist) == 0:
        return []

    result, _ = zip(*search_dist)
    return list(set(result))


def search(request):
    if request.method['GET']:
        return JsonResponse({
            "result_code": 200,
            "results": searching(request.GET['object'], request.GET['search'], 10)
        })


def search2(request):
    shops = Shop.objects.all().filter(user_owner=request.user)
    if request.method == 'GET':
        type = request.GET.get('type')
        query = request.GET.get('q')
        if type == "product":
           list_items = Product.objects.filter(nameProduct__icontains=query)
        elif type == "shop":
            list_items = Shop.objects.filter(shop_name__icontains=query)
        else:
            list_items = User.objects.filter(username__icontains=query)

        context = {
            "list_items": list_items,
            "list_shops": shops,
            "type": type,
        }

        return render(request, 'petsy/show_products.html', context)


@login_required()
def edit_user(request):
    user = UserPetsy.objects.get(id_user=request.POST['username'])
    if request.POST['modify'] == 'description':
        user.description = request.POST['description']
        return JsonResponse({
            "result_code": 200
        })


def edit_shop(request):
    shop = Shop.objects.get(id_shop=request.POST['id_shop'])
    if request.POST['modify'] == 'shop_name':
        shop.shop_name = request.POST['shop_name']

    elif request.POST['modify'] == 'description':
        shop.description = request.POST['description']

    return JsonResponse({
        "result_code": 200
    })


def edit_product(request):
    product = Product.objects.get(idProduct=request.POST['id_product'])
    if request.POST['modify'] == 'nameProduct':
        product.nameProduct = request.POST['nameProduct']

    elif request.POST['modify'] == 'description':
        product.description = request.POST['description']

    elif request.POST['modify'] == 'price':
        product.price = request.POST['price']

    # elif request.POST['modify'] == 'featured_photo:

    return JsonResponse({
        "result_code": 200
    })


def cesta_add_product_by_id(request):
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
    id_product = request.POST['id_product']
    amount = request.POST['amount']
    usern = request.user  # "joseluis"  # request.POST['username']

    user = UserPetsy.objects.get(username=usern)
    current_bill = user.currentBill

    current_bill += str(id_product)+"-"+str(amount)+","

    user.currentBill = current_bill
    user.save()
    print(current_bill)
    return redirect(get_product_by_id, id_product=id_product)


def render_bill(request):
    print(request.user)
    us = UserPetsy.objects.get(username=request.user)
    current_bill = us.currentBill
    obj_dict = {}

    print("BBBBBBBBBBBBBBBBBBBBBBB")
    print("BBBBBBBBBBBBBBBBBBBBBBB")
    print("BBBBBBBBBBBBBBBBBBBBBBB")
    print("BBBBBBBBBBBBBBBBBBBBBBB")

    print(current_bill)
    total = 0
    for pair in current_bill.split(','):  # id-amount,id-amount

        if pair != '':
            print(pair)
            id = pair.split('-')[0]
            amount = pair.split('-')[1]
            prod = Product.objects.get(idProduct=id)
            obj_dict[id] = {
                "id": id,
                "name": prod.nameProduct,
                "price": prod.price,
                "amount": amount,
                "totalPrice": int(amount)*prod.price
            }
            total += float(obj_dict[id]["totalPrice"])
    obj_dict["fin"] = {
        "name": "",
        "price": "",
        "amount": "",
        "totalPrice": total
    }
    return render(request, 'petsy/bill.html', {"patata": list(obj_dict.values())})

def bill_dict(request):
    current_bill = UserPetsy.objects.get(username=request.user).currentBill
    obj_dict = {}

    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA")


    for pair in current_bill.split(','):  # id-amount,id-amount
        if pair != '':
            id = pair.split('-')[0]
            amount = pair.split('-')[1]
            prod = Product.objects.get(idProduct=id)
            obj_dict[id] = {
                "id": id,
                "name": prod.nameProduct,
                "price": prod.price,
                "amount": amount,
                "totalPrice": int(amount) * prod.price
            }

    return obj_dict