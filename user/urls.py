from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("register/", views.register_view, name='register_view'),
    path("login/", views.login_view, name='login_view'),
    path("logout/", views.custom_logout, name='custom_logout'),
    # path("account", views.account, name="account"),
    path("account/update", views.account_update, name="account_update"),
    # path("account/my-product", views.my_product, name="my_product"),
    # path("account/add-product", views.add_product, name="add_product"),
]