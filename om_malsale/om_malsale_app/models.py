from django.db import models
from cloudinary.models import CloudinaryField


class Product(models.Model):
    name = models.CharField(max_length=200)
    image = CloudinaryField('image')

    # Product weight, e.g. 200g
    weight = models.CharField(max_length=50, default="200g")

    # MRP and our selling price
    mrp = models.FloatField()
    sale_price = models.FloatField(default=0)

    # Product display information
    discount_percent = models.PositiveIntegerField(default=25)
    discount_text = models.CharField(
        default="Best Price!",
        max_length=100
    )
    rating = models.FloatField(default=4.5)
    review_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def pack10_price(self):
        """Calculate price for a pack of 10."""
        return round(self.sale_price * 10, 2)


class Order(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    items = models.TextField(default="")
    total = models.FloatField()

    # Order status
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("confirmed", "Confirmed"),
            ("out_for_delivery", "Out for Delivery"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        default="pending",
    )

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name