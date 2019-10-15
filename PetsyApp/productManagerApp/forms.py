from django import forms
from .models import Product, Review
from django.forms import Textarea, NumberInput, TextInput, DateTimeInput
from django.forms import ValidationError


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['idProduct', 'nameProduct', 'description', 'price_average', 'category', 'materials']



class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ["title", "message", "rating"]

        widgets = {
            "title": TextInput(attrs={'class': 'form-control', 'style': 'width:100%; resize:none'}),
            "message": Textarea(attrs={'class': 'form-control', 'rows': 3, 'style': 'width:100%; resize:none'}),
            # "date": DateTimeInput(attrs={'class': 'form-control', 'style': 'width:100%; resize:none'}) ,
            "rating": NumberInput(attrs={'min': '1', 'max': '5', 'default': 1, 'style': 'display:none'})
        }
        


    def clean_message(self):
        """
        Check that the message contains at least one character. If not, adds an error to the form.
        :return: Message of the review
        """
        message = self.cleaned_data["message"]
        if len(message) <= 0:
            self.add_error("message", "You can't send an empty message")
            raise ValidationError("You can't send an empty message")
        return message


class Shop(forms.ModelForm):
    model = Product
    fields = ['shop_name']