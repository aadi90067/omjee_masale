from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "mrp", "pack1_price", "pack3_price", "pack6_price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "show_items", "total", "created")
    readonly_fields = ("name", "phone", "address", "show_full_items", "total", "created")

    fieldsets = (
        ("Customer Details", {
            "fields": ("name", "phone", "address")
        }),
        ("Order Details", {
            "fields": ("show_full_items", "total", "created")
        }),
    )

    def show_items(self, obj):
        if obj.items:
            return obj.items
        return "-"
    show_items.short_description = "Items"

    def show_full_items(self, obj):
        if obj.items:
            return format_html("<br>".join(obj.items.split("\n")))
        return "-"
    show_full_items.short_description = "Ordered Items"