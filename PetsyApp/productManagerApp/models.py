from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


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
    idProduct = models.DecimalField(max_digits=5, decimal_places=3)
    description = models.CharField(max_length=1000)
    category = models.CharField(max_length=5, choices=CATEGORIES)
    price_average = models.DecimalField(max_digits=5, decimal_places=3)
    materials = models.TextField()
    sold = models.IntegerField()
    # By default assign a house image to the product
    # featured_photo = models.ImageField(upload_to="photos", default="static/images/etsy.png")
    rate = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    num_votes = models.IntegerField() # número persones que han votat un producte
    sum_votes = models.IntegerField() # suma total del rate dels productes

    def get_human_category(self):
        return self._d_categories[self.category]


class Review(models.Model):
    id_rev = models.AutoField(primary_key=True)
    # Relation between the User and the Review
    user_rev = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    message = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1,
                                 validators=[MinValueValidator(1, "Value must be between 1 and 5"),
                                            MaxValueValidator(5, "Value must be between 1 and 5")])
