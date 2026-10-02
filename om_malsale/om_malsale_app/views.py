from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product, Order


def welcome(request):
    return render(request, "welcome.html")


def index(request):
    query = request.GET.get("q", "").strip()

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all().order_by("-id")

    return render(request, "index.html", {
        "products": products,
        "query": query
    })


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    return render(request, "product_detail.html", {
        "p": product
    })


def add_cart(request):
    if request.method != "POST":
        return JsonResponse(
            {"status": "invalid request"},
            status=400
        )

    pid = request.POST.get("pid")
    qty = request.POST.get("qty", "1")

    try:
        qty = int(qty)
    except (ValueError, TypeError):
        qty = 1

    if qty < 1:
        qty = 1

    product = get_object_or_404(Product, id=pid)

    cart = request.session.get("cart", {})

    # Only Pack of 10
    pack_name = "Pack of 10"
    price = product.pack10_price

    # One cart item per product
    key = f"{product.id}_10"

    if key in cart:
        cart[key]["qty"] += qty
    else:
        cart[key] = {
            "product_id": product.id,
            "name": product.name,
            "image": product.image.url if product.image else "",
            "price": float(price),
            "qty": qty,
            "pack": pack_name,
            "weight": product.weight,
        }

    request.session["cart"] = cart
    request.session.modified = True

    cart_count = sum(
        item["qty"] for item in cart.values()
    )

    return JsonResponse({
        "status": "added",
        "cart_count": cart_count
    })


def cart(request):
    cart_data = request.session.get("cart", {})

    items = []
    total = 0

    for key, item in cart_data.items():
        subtotal = item["price"] * item["qty"]

        item_data = item.copy()
        item_data["subtotal"] = subtotal
        item_data["key"] = key

        total += subtotal
        items.append(item_data)

    return render(request, "cart.html", {
        "items": items,
        "total": total
    })


def increase_qty(request, key):
    cart = request.session.get("cart", {})

    if key in cart:
        cart[key]["qty"] += 1

        request.session["cart"] = cart
        request.session.modified = True

    return redirect("cart")


def decrease_qty(request, key):
    cart = request.session.get("cart", {})

    if key in cart:
        if cart[key]["qty"] > 1:
            cart[key]["qty"] -= 1
        else:
            del cart[key]

        request.session["cart"] = cart
        request.session.modified = True

    return redirect("cart")


def remove_item(request, key):
    cart = request.session.get("cart", {})

    if key in cart:
        del cart[key]

        request.session["cart"] = cart
        request.session.modified = True

    return redirect("cart")


def checkout(request):
    cart = request.session.get("cart", {})

    if not cart:
        return redirect("cart")

    total = 0
    items_text = ""

    for item in cart.values():
        subtotal = item["price"] * item["qty"]
        total += subtotal

        items_text += (
            f"{item['name']} ({item['pack']}) "
            f"x {item['qty']} = ₹{subtotal}\n"
        )

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()

        if name and phone and address:

            # Create order
            order = Order.objects.create(
                name=name,
                phone=phone,
                address=address,
                items=items_text.strip(),
                total=total,
                status="pending"
            )

            # Save order information in session
            request.session["last_order_id"] = order.id
            request.session["last_order_name"] = name
            request.session["last_order_phone"] = phone

            # Clear cart after successful order
            request.session["cart"] = {}
            request.session.modified = True

            # Go to order success page
            return redirect("order_success")

    return render(request, "checkout.html", {
        "total": total
    })


def order_success(request):
    order_id = request.session.get("last_order_id")

    if not order_id:
        return redirect("home")

    order = get_object_or_404(Order, id=order_id)

    return render(request, "order_success.html", {
        "order": order
    })


def track_orders(request):
    orders = None

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()

        if name and phone:
            orders = Order.objects.filter(
                name__iexact=name,
                phone=phone
            ).order_by("-created")

    else:
        last_name = request.session.get("last_order_name")
        last_phone = request.session.get("last_order_phone")

        if last_name and last_phone:
            orders = Order.objects.filter(
                name__iexact=last_name,
                phone=last_phone
            ).order_by("-created")

    return render(request, "track_orders.html", {
        "orders": orders
    })