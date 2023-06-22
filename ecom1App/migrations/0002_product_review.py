# Generated by Django 4.1.4 on 2023-04-11 08:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecom1App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('referenceNum', models.CharField(max_length=255)),
                ('brand', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, default='/sample.jpg', null=True, upload_to='')),
                ('actualPrice', models.DecimalField(decimal_places=2, max_digits=9)),
                ('sellingPrice', models.DecimalField(decimal_places=2, max_digits=9)),
                ('rating', models.DecimalField(decimal_places=2, max_digits=7)),
                ('numReviews', models.IntegerField(default=0)),
                ('description', models.TextField(blank=True, null=True)),
                ('countInStock', models.IntegerField(default=0)),
                ('category', models.CharField(max_length=200)),
                ('subCategory', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewTitle', models.CharField(max_length=255)),
                ('writtenReview', models.TextField(blank=True, null=True)),
                ('rating', models.IntegerField(default=0)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecom1App.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
