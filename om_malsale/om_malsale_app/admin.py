from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "image_preview",
        "name",
        "mrp",
        "pack1_price",
        "pack3_price",
        "pack6_price",
        "rating",
        "review_count",
        "discount_percent",
        "discount_text",
    )

    search_fields = ("name",)
    list_editable = ("rating", "review_count", "discount_percent", "discount_text")
    readonly_fields = ("image_preview_large",)

    fieldsets = (
        ("Product Details", {
            "fields": ("name", "image", "image_preview_large")
        }),
        ("Pricing", {
            "fields": ("mrp", "pack1_price", "pack3_price", "pack6_price")
        }),
        ("Rating & Reviews", {
            "fields": ("rating", "review_count")
        }),
        ("Offer / Discount", {
            "fields": ("discount_percent", "discount_text")
        }),
    )

    def image_preview(self, obj):
        try:
            if obj.image:
                return format_html(
                    '<img src="{}" width="55" height="55" style="border-radius:8px; object-fit:cover;" />',
                    obj.image.url
                )
        except:
            pass
        return "-"
    image_preview.short_description = "Image"

    def image_preview_large(self, obj):
        try:
            if obj.image:
                return format_html(
                    '<img src="{}" width="180" style="border-radius:12px; object-fit:cover;" />',
                    obj.image.url
                )
        except:
            pass
        return "-"
    image_preview_large.short_description = "Preview"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "show_items", "total", "created")
    search_fields = ("name", "phone")
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
            first_line = obj.items.split("\n")[0]
            if len(obj.items.split("\n")) > 1:
                return f"{first_line} ..."
            return first_line
        return "-"
    show_items.short_description = "Items"

    def show_full_items(self, obj):
        if obj.items:
            return format_html("<br>".join(obj.items.split("\n")))
        return "-"
    show_full_items.short_description = "Ordered Items"