from django.urls import path
from . import views

urlpatterns = [
    path("create/",views.created_product,name="created_product"),
    path("my-product/",views.my_product, name="my_product"),
]