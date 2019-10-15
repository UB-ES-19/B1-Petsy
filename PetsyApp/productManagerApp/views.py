from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import CreateView

from django.urls import reverse_lazy

from .models import Product

'''
class ProductListView(ListView):
    model = Product
    # template_name = 'productManagerApp/list'


class ProductDetailView(DetailView):
    model = Product
    


class ProductCreate(CreateView):
    model = Product
    fields = ['name', 'description', 'price', 'category']


class ProductUpdate(UpdateView):
    model = Product
    fields = ['name', 'description', 'price', 'category']


class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('list_product')


def MyProducts(ListView):
    template_name = 'productManagerApp/list'
'''

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

        return JsonResponse({
            "product": {
                "name": product.nameProduct,
                "description": product.description,
                "category": product.category,
                "price_average": product.price_average,
                "materials": product.materials,
                "sold": product.sold,
                "photo": product.featured_photo,
                "num_votes": product.num_votes,
                "sum_votes": product.sum_votes
            },
            "response_code": 200
        })


def rate_product_by_id(request):
    """
    That function expects a request with the following body:
        {
            "product_id": 4,
            "rate": 3.5
        }
    And then, updates the field 'sum_votes' and 'num_votes' from the 'product_id' product.

    :param request
    :return: JsonResponse
    """
    id_product = request.POST['product_id']
    product_to_update = Product.objects.get(idProduct=id_product)
    new_rate = request.POST['rate']

    updated_sum_votes = product_to_update.sum_votes + new_rate
    updated_num_votes = product_to_update.num_votes + 1

    Product.objects.\
        filter(idProduct=id_product).\
        update(sum_votes=updated_sum_votes, num_votes=updated_num_votes)

    return JsonResponse({
        "response_code": 200
    })


def review_product_by_id(request):
    """
    That function expects a request with the following body:
        {
            "product_id": 4,
            "review": "Very good quality, I really recommend it bc..."
        }
    And then, updates the field 'reviews' from the 'product_id' product.

    :param request
    :return: JsonResponse
    """
    id_product = request.POST['product_id']
    product_to_update = Product.objects.get(idProduct=id_product)
    new_review = request.POST['review']

    actual_reviews = product_to_update.reviews


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