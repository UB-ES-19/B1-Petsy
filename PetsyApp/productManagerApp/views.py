from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import CreateView

from django.urls import reverse_lazy

from .models import Product, Shop
import ast
import time


def index(request):
    return render(request, 'petsy/product.html')


def get_product_by_id(request, id_product=None):
    """
    :param request:
    :param id_product:
    :return:
    """

    products = Product.objects.all()

    print("\n**********************")
    for product in products:
        print("Name: ", product.nameProduct)
        print("Shop_id: ", product.id_shop)
        print("Reviews: ", product.reviews)
        print("id_product: ", product.idProduct)
        print("rating: ", product.sum_votes / product.num_votes if product.num_votes != 0 else 0)
        print()
    print("**********************\n")

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
        # aqui hauriem de redirigir a una url per mostrar el producte.
        # return HttpResponseRedirect('', {
        #     "product": {
        #         "name": product.nameProduct,
        #         "description": product.description,
        #         "category": product.category,
        #         "price_average": product.price,
        #         "materials": product.materials,
        #         "sold": product.sold,
        #         "photo": product.featured_photo,
        #         "num_votes": product.num_votes,
        #         "sum_votes": product.sum_votes,
        #         "shop_id": product.id_shop
        #     },
        #     "response_code": 200
        # })

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

    return render(request, 'petsy/userpage.html', {
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

        shop = Shop.objects.get(user_owner=user)
        print("Cosas de shop")
        product_name = (request.POST['titulo'])
        img = (request.POST['img'])
        descripcio = request.POST['descripcion']
        price = request.POST['precio']
        category = request.POST['categoria']
        material = request.POST['materiales']
        print("Cosas de product variables")
        # save product into database
        product = Product(
            nameProduct=product_name,
            featured_photo=img,
            description=descripcio,
            price=price,
            category=category,
            materials=material,
            # sold=0,
            id_shop=shop.id_shop
        )
        product.save()
        print("pre httpresponse")

        return HttpResponseRedirect('id/' + str(product.idProduct), {
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

        # return render(request, 'petsy/product.html', {
        #     "titulo": product.nameProduct,
        #     "descripcion": product.description,
        #     "categoria": product.category,
        #     "precio": product.price,
        #     "materiales": product.materials,
        #     "img": product.featured_photo,
        #     "num_votes": product.num_votes,
        #     "sum_votes": product.sum_votes,
        #     "shop_id": product.id_shop,
        #     "reviews": ast.literal_eval(product.reviews),
        #     "product_id": product.idProduct
        # })

    return HttpResponse('')
