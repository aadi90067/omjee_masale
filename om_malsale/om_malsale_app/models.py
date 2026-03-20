from django.db import models
from cloudinary.models import CloudinaryField


class Product(models.Model):
    name = models.CharField(max_length=200)
    image = CloudinaryField('image')
    mrp = models.FloatField()

    pack1_price = models.FloatField()
    pack3_price = models.FloatField()
    pack6_price = models.FloatField()

    # Admin controlled rating
    rating = models.FloatField(default=4.5)
    review_count = models.PositiveIntegerField(default=0)

    # Admin controlled discount
    discount_percent = models.PositiveIntegerField(default=25)
    discount_text = models.CharField(
        max_length=100,
        default="Best Price!"
    )

    def __str__(self):
        return self.name

    @property
    def pack3_unit_price(self):
        return round(self.pack3_price / 3, 2)

    @property
    def pack6_unit_price(self):
        return round(self.pack6_price / 6, 2)

    @property
    def full_discount_text(self):
        return f"Save {self.discount_percent}% - {self.discount_text}"

    @property
    def rating_stars(self):
        r = float(self.rating)

        if r >= 4.75:
            return "⭐⭐⭐⭐⭐"
        elif r >= 4.25:
            return "⭐⭐⭐⭐✨"
        elif r >= 3.75:
            return "⭐⭐⭐⭐☆"
        elif r >= 3.25:
            return "⭐⭐⭐✨☆"
        elif r >= 2.75:
            return "⭐⭐⭐☆☆"
        elif r >= 2.25:
            return "⭐⭐✨☆☆"
        elif r >= 1.75:
            return "⭐⭐☆☆☆"
        elif r >= 1.25:
            return "⭐✨☆☆☆"
        elif r >= 0.75:
            return "⭐☆☆☆☆"
        else:
            return "No Rating"
        

class Order(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    items = models.TextField(default="")
    total = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name