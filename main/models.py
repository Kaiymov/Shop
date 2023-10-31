from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=100, unique=True, verbose_name='Телефон номер')
    telegram_id = models.PositiveIntegerField(blank=True, null=True)
    activate_code = models.CharField(max_length=6, blank=True)

    @property
    def create_code(self):
        import random
        return random.randint(100_000, 999_999)


class Category(models.Model):
    image = models.ImageField(upload_to='category_img/', blank=True)
    name = models.CharField(max_length=50, unique=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=50, primary_key=True, blank=True, verbose_name='Уникальное название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class CategoryBrand(models.Model):
    image = models.ImageField(upload_to='category_brand_img/', blank=True)
    category_parent = models.ForeignKey(Category, related_name='category_parent', on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=50, unique=True, blank=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=50, primary_key=True, blank=True, verbose_name='Уникальное название')

    def __str__(self):
        return f'{self.category_parent} - {self.name}'

    class Meta:
        verbose_name = 'Категория бренда'
        verbose_name_plural = 'Категории бренда'


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE, verbose_name='Категория')
    category_brand = models.ForeignKey(CategoryBrand, related_name='category_brend', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField('Название продукта', max_length=255)
    status = models.BooleanField('Cтатус', default=True)
    color = models.CharField('Цвет', max_length=100, default='Черный')
    price = models.IntegerField('Цена')
    time_create = models.DateField('Дата создание', auto_now_add=True)
    image = models.ImageField('Картина', upload_to='product_img', blank=True, null=True)
    description = models.TextField('Описание')

    def __str__(self):
        return f'{self.category} {self.title}'

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except Exception:
            url = 'static/img/no_img.png'
        return url


    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    text = models.TextField()