from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name='home'),
    path("register/", views.register_view, name='register_view'),
    path("login/", views.login_view, name='login_view'),
    path("logout/", views.custom_logout, name='custom_logout'),
    # path("account", views.account, name="account"),
    path("account/update", views.account_update, name="account_update"),


    # Nhập email
    path("forgot-password/", auth_views.PasswordResetView.as_view(template_name="user/forgot_password.html",
        email_template_name="user/password_reset_email.html",
        subject_template_name="user/password_reset_subject.txt",
        success_url=reverse_lazy("password_reset_done")),
         name="forgot_password"),
    # Sau khi bấm confirm 
    path("password-reset-done/",auth_views.PasswordResetDoneView.as_view(
            template_name="user/password_reset_done.html"),
        name="password_reset_done"),
    # link được gửi trong mail sẽ chạy vào đây 
    path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(
            template_name="user/password_reset_confirm.html"),
        name="password_reset_confirm"),
        path("reset/done/",auth_views.PasswordResetCompleteView.as_view(
        template_name="user/password_reset_complete.html"
    ),
    name="password_reset_complete"
    ),  
    

]