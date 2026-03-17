from django.urls import path
from . import views

urlpatterns = [

    path('', views.welcome, name="welcome"),   # 👈 FIRST PAGE
    path('home/', views.index, name="home"),   # 👈 PRODUCTS PAGE

path("product/<int:id>/",views.product_detail,name="product_detail"),

path("add-cart/",views.add_cart,name="add_cart"),

path("cart/",views.cart,name="cart"),

path("increase/<str:key>/",views.increase_qty,name="increase"),

path("decrease/<str:key>/",views.decrease_qty,name="decrease"),

path("remove/<str:key>/",views.remove_item,name="remove"),

path("checkout/",views.checkout,name="checkout"),

]