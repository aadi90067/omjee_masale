from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Order


# =========================
# PRODUCT ADMIN
# =========================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "weight",
        "mrp",
        "sale_price",
        "pack10_price",
    )

    fields = (
        "name",
        "image",
        "weight",
        "mrp",
        "sale_price",
    )


# =========================
# ORDER ADMIN
# =========================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "phone",
        "address",
        "show_items",
        "total",
        "status",
        "created",
    )

    list_editable = ("status",)

    search_fields = (
        "name",
        "phone",
        "address",
    )

    list_filter = (
        "status",
        "created",
    )

    date_hierarchy = "created"

    ordering = ("-created",)

    readonly_fields = (
        "name",
        "phone",
        "address",
        "show_full_items",
        "total",
        "created",
    )

    fieldsets = (
        (
            "Customer Details",
            {
                "fields": (
                    "name",
                    "phone",
                    "address",
                )
            },
        ),
        (
            "Order Details",
            {
                "fields": (
                    "show_full_items",
                    "total",
                    "status",
                    "created",
                )
            },
        ),
    )

    # Quick actions
    actions = (
        "mark_confirmed",
        "mark_out_for_delivery",
        "mark_completed",
        "mark_cancelled",
    )

    @admin.action(description="✅ Confirm selected orders")
    def mark_confirmed(self, request, queryset):
        queryset.update(status="confirmed")

    @admin.action(description="🚚 Mark selected as Out for Delivery")
    def mark_out_for_delivery(self, request, queryset):
        queryset.update(status="out_for_delivery")

    @admin.action(description="✅ Mark selected as Completed")
    def mark_completed(self, request, queryset):
        queryset.update(status="completed")

    @admin.action(description="❌ Cancel selected orders")
    def mark_cancelled(self, request, queryset):
        queryset.update(status="cancelled")

    def show_items(self, obj):
        if obj.items:
            return obj.items
        return "-"

    show_items.short_description = "Items"

    def show_full_items(self, obj):
        if obj.items:
            return format_html(
                "<br>".join(obj.items.split("\n"))
            )
        return "-"

    show_full_items.short_description = "Ordered Items"