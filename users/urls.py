from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import (
    new_password,
    email_verification,
    UserCreateView,
    UserListView,
    UserDetailView,
    UserUpdateView,
    UserDeleteView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("email-confirm/<str:token>/", email_verification, name="email_confirm"),
    path("new-password/", new_password, name="new_password"),
    path("users-list/", UserListView.as_view(), name="users_list"),
    path("user-detail/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("user-change/<int:pk>/", UserUpdateView.as_view(), name="user_change"),
    path("user-delete/<int:pk>/", UserDeleteView.as_view(), name="user_delete"),
]
