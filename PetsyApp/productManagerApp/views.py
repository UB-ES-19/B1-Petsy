from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import CreateView

from django.urls import reverse_lazy

from .models import Product

class ProductListView(ListView):
    model = Product
    #template_name = 'productManagerApp/list'


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

