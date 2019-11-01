# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-11-01 20:15
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import productManagerApp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('nameProduct', models.CharField(max_length=30)),
                ('idProduct', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=1000)),
                ('category', models.CharField(choices=[('Joya', 'Joyeria y complementos'), ('Ropa', 'Ropa y calzado'), ('Casa', 'Hogar y decoracion'), ('Boda', 'Bodas y fiestas'), ('Toys', 'Juguetes y ocio'), ('Cole', 'Arte y objetos de decoración'), ('Arte', 'Herramientas para la artesania'), ('Vint', 'Vintage'), ('Otro', 'Otras categorias')], default='Otro', max_length=5)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('materials', models.TextField(default='')),
                ('sold', models.IntegerField(default=0)),
                ('img', models.ImageField(upload_to=productManagerApp.models.get_image_filename_post)),
                ('rate', models.DecimalField(decimal_places=1, default=0, max_digits=3)),
                ('num_votes', models.IntegerField(default=0)),
                ('sum_votes', models.IntegerField(default=0)),
                ('reviews', models.TextField(default='[]')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('date', models.DateTimeField()),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2, validators=[django.core.validators.MinValueValidator(1, 'Value must be between 1 and 5'), django.core.validators.MaxValueValidator(5, 'Value must be between 1 and 5')])),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productManagerApp.Product')),
                ('user_rev', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id_shop', models.AutoField(primary_key=True, serialize=False)),
                ('shop_name', models.TextField(default='Shop')),
                ('user_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productManagerApp.Shop'),
        ),
    ]
