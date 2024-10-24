import secrets

from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)

from config.settings import EMAIL_HOST_USER
from users.forms import (
    UserCreateForm,
    UserForm,
    UserUpdateForm,
    UserUpdateModeratorForm,
)
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет! Перейди по ссылке, чтобы подтвердить свою почту {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return super().form_valid(form)


class UserListView(ListView):
    model = User


class UserDetailView(DetailView):
    model = User
    form_class = UserForm


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User

    def get_success_url(self):
        return reverse("users:user_detail", args=[self.kwargs.get("pk")])

    def get_form_class(self):
        user = self.request.user
        if user == self.object:
            return UserUpdateForm
        if user.has_perm("users.lock_user"):
            return UserUpdateModeratorForm
        raise PermissionDenied


class UserDeleteView(DeleteView):
    model = User


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()

    return redirect(reverse("users:login"))


def new_password(request):
    if request.method == "POST":
        email = request.POST["email"]
        user = get_object_or_404(User, email=email)

        new_pass = secrets.token_hex(6)
        user.password = make_password(new_pass)
        user.save()
        send_mail(
            subject="Смена пароля",
            message=f"На аккаунте установлен новый пароль: {new_pass}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return redirect(reverse("users:login"))
    return render(request, "users/new_password.html")
