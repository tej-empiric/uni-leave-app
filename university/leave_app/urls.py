from django.urls import path
from . import views
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

# app_name = "leave_app"
urlpatterns = [
    path("", views.loginPage, name="login"),
    path("register/", views.register, name="register"),
    path("user/", views.user, name="user"),
    path("user/leave_status/", views.leaveStatus, name="leave_status"),
    path("<int:id>/", views.change_status, name="change_status"),
    path("forget/", views.forget, name="forget"),
    path("logout/", views.logoutPage, name="logout"),
    path(
        "password-reset/",
        PasswordResetView.as_view(template_name="leave_app/password_reset.html"),
        name="password-reset",
    ),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(
            template_name="leave_app/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="leave_app/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        PasswordResetCompleteView.as_view(
            template_name="leave_app/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]





