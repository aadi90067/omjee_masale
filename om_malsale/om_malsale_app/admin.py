from django.contrib import admin
from .models import Product, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "mrp", "pack1_price", "pack3_price", "pack6_price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "short_items", "total", "created")
    readonly_fields = ("name", "phone", "address", "items", "total", "created")

    fieldsets = (
        ("Customer Details", {
            "fields": ("name", "phone", "address")
        }),
        ("Order Details", {
            "fields": ("items", "total", "created")
        }),
    )

    def short_items(self, obj):
        if obj.items:
            return obj.items[:40] + "..." if len(obj.items) > 40 else obj.items
        return "-"
    short_items.short_description = "Items"