from django.urls import path
from . import views

urlpatterns = [
    path("create/",views.created_product,name="created_product"),
    path("my-product/",views.my_product, name="my_product"),
    path("update/<int:id>/",views.update_product,name="update_product"),
    path("delete-product/<int:id>/", views.delete_product, name="delete_product"),
    path("detail/<int:id>/", views.product_detail, name="product_detail"),
    path("add-to-cart/",views.add_to_cart,name="add_to_cart"),
    path("cart", views.cart, name="cart"),
    path("cart/update", views.update_cart, name="update_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("search/", views.search_product, name="search_product")
]