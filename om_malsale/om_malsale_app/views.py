from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product, Order
from django.core.mail import send_mail


# HOME PAGE
def index(request):

    products = Product.objects.all()

    return render(request,"index.html",{
        "products":products
    })


# PRODUCT DETAIL
def product_detail(request,id):

    p = get_object_or_404(Product,id=id)

    return render(request,"product_detail.html",{
        "p":p
    })


# ADD TO CART
def add_cart(request):

    if request.method == "POST":

        pid = request.POST.get("pid")
        pack = request.POST.get("pack")
        qty = int(request.POST.get("qty"))

        product = Product.objects.get(id=pid)

        cart = request.session.get("cart",{})

        if pack == "1":
            price = product.pack1_price
            pack_name = "1 Pack"

        elif pack == "3":
            price = product.pack3_price
            pack_name = "3 Pack"

        else:
            price = product.pack6_price
            pack_name = "6 Pack"

        key = f"{pid}_{pack}"

        if key in cart:

            cart[key]["qty"] += qty

        else:

            cart[key] = {
                "name":product.name,
                "image":product.image.url if product.image else "",
                "price":price,
                "qty":qty,
                "pack":pack_name
            }

        request.session["cart"] = cart

        return JsonResponse({"status":"added"})


# CART PAGE
def cart(request):

    cart = request.session.get("cart",{})

    items = []
    total = 0

    for key,item in cart.items():

        subtotal = item["price"] * item["qty"]

        item["subtotal"] = subtotal
        item["key"] = key

        total += subtotal

        items.append(item)

    return render(request,"cart.html",{

        "items":items,
        "total":total

    })


# INCREASE QTY
def increase_qty(request,key):

    cart = request.session.get("cart",{})

    if key in cart:

        cart[key]["qty"] += 1

    request.session["cart"] = cart

    return redirect("cart")


# DECREASE QTY
def decrease_qty(request,key):

    cart = request.session.get("cart",{})

    if key in cart:

        if cart[key]["qty"] > 1:
            cart[key]["qty"] -= 1
        else:
            del cart[key]

    request.session["cart"] = cart

    return redirect("cart")


# REMOVE ITEM
def remove_item(request,key):

    cart = request.session.get("cart",{})

    if key in cart:

        del cart[key]

    request.session["cart"] = cart

    return redirect("cart")


# CHECKOUT
def checkout(request):

    cart = request.session.get("cart", {})

    items_text = ""
    total = 0

    for key, item in cart.items():

        subtotal = item["price"] * item["qty"]
        total += subtotal

        items_text += f"{item['name']} ({item['pack']}) x {item['qty']} = ₹{subtotal}\n"


    if request.method == "POST":

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        # Save Order
        Order.objects.create(
            name=name,
            phone=phone,
            address=address,
            total=total
        )

        # Email message
        message = f"""
New Order Received - Om Masale

Customer Name: {name}
Phone: {phone}

Address:
{address}

Items Ordered:
{items_text}

Total Amount: ₹{total}
"""

        send_mail(
            subject="New Order - Om Masale",
            message=message,
            from_email="yourgmail@gmail.com",
            recipient_list=["yourgmail@gmail.com"],
        )

        request.session["cart"] = {}

        return render(request, "success.html")

    return render(request, "checkout.html", {
        "total": total
    })

