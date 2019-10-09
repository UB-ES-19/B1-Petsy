from django.db import models

# Create your models here.

from django.db import models


class Product(models.Model):
    CATEGORIES = (
        ("Joya", "Joyeria y complementos"),
        ("Ropa", "Ropa y calzado"),
        ("Casa", "Hogar y decoracion"),
        ("Boda", "Bodas y fiestas"),
        ("Toys", "Juguetes y ocio"),
        ("Cole", "Arte y objetos de decoración"),
        ("Arte", "Herramientas para la artesania"),
        ("Vint", "Vintage"),
        ("Otro", "Otras categorias")
    )
    _d_categories = dict(CATEGORIES)

    nameProduct = models.CharField(max_length=30)
    idProduct = models.DecimalField(max_length=5, decimal_places=3)
    description = models.CharField(max_length=1000)
    category = models.CharField(max_length=5, choices=CATEGORIES)
    price_average = models.DecimalField(max_digits=5, decimal_places=3)
    materials = models.TextField()
    sold = models.BooleanField()
    # By default assign a house image to the product
    featured_photo = models.ImageField(upload_to="photos", default="static/images/etsy.png")
    rate = models.DecimalField(max_digits=3, decimal_places=1, default=0)

    def get_human_category(self):
        return self._d_categories[self.category]
