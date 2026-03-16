from django.db import models


class Product(models.Model):

    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="products/")
    mrp = models.FloatField()

    pack1_price = models.FloatField()
    pack3_price = models.FloatField()
    pack6_price = models.FloatField()

    def __str__(self):
        return self.name

    # ⭐ Per unit price calculation

    @property
    def pack3_unit_price(self):
        return round(self.pack3_price / 3, 2)

    @property
    def pack6_unit_price(self):
        return round(self.pack6_price / 6, 2)


class Order(models.Model):

    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    total = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name