from django.db import models

# Create your models here.


class Client(models.Model):
    name = models.CharField(max_length=50)
    login = models.CharField(max_length=20, unique=True)
    # password = models.CharField(max_length=8)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    # avatar = models.ImageField(default='{PWD}/FlowerLight/static/img/default_avatar.svg')

    def __str__(self):
        return self.login


class Product(models.Model):
    BOUQUET = 0
    SEPARATED_FLOWER = 1
    ALIVE_FLOWER = 2
    SEEDS = 3

    BOUQUET_NAME = 'букеты'
    SEPARATED_FLOWER_NAME = 'срезанные отдельные цветы'
    ALIVE_FLOWER_NAME = 'живые цветы'
    SEEDS_NAME = 'семена'

    PRODUCT_TYPE_CHOICES = (
        (BOUQUET, BOUQUET_NAME),
        (SEPARATED_FLOWER, SEPARATED_FLOWER_NAME),
        (ALIVE_FLOWER, ALIVE_FLOWER_NAME),
        (SEEDS, SEEDS_NAME)
    )

    name = models.CharField(max_length=50)
    type = models.IntegerField(choices=PRODUCT_TYPE_CHOICES,
                               default=BOUQUET)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(null=True)
    image = models.ImageField(default='productPictures/default_flower_image.jpg', upload_to='productPictures')

    def __str__(self):
        return self.name


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    order_date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField()

    def __str__(self):
        return '{}: {} - {}'.format(self.order_date, self.client, self.product)





