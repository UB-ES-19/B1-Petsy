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
    idProduct = models.AutoField(primary_key=True)
    description = models.CharField(max_length=1000)
    category = models.CharField(max_length=5, choices=CATEGORIES, default='Otro')
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    materials = models.TextField(default='')
    sold = models.IntegerField(default=0)
    # By default assign a house image to the product
    featured_photo = models.FileField(upload_to="photos/", default="etsy.png")
    rate = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    num_votes = models.IntegerField(default=0)  # numero persones que han votat un producte
    sum_votes = models.IntegerField(default=0)  # suma total del rate dels productes
    id_shop = models.IntegerField(default=0)
    reviews = models.TextField(default='[]')

    def get_human_category(self):
        return self._d_categories[self.category]


class Shop(models.Model):
    id_shop = models.AutoField(primary_key=True)
    shop_name = models.TextField(default='Shop')
    user_owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Review(models.Model):
    # id_rev = models.AutoField(primary_key=True)
    # Relation between the User and the Review
    title_message = models.CharField(max_length=100, blank=False)
    message = models.TextField()
    date = models.DateTimeField()
    rating = models.DecimalField(max_digits=2,
                                 decimal_places=1,
                                 validators=[MinValueValidator(1, "Value must be between 1 and 5"),
                                             MaxValueValidator(5, "Value must be between 1 and 5")
                                             ]
                                 )
    user_rev = models.ForeignKey(User)
    product = models.ForeignKey(Product)


