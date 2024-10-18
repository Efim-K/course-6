import secrets
import random
import string

from django.core.mail import send_mail
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect

from users.forms import UserRegisterForm, ResetPasswordForm, UserProfileForm, StyleFormMixin
from users.models import User

from django.contrib.auth.views import PasswordResetView

from config.settings import EMAIL_HOST_USER


# Create your views here.
class UserCreateView(CreateView, StyleFormMixin):
    """
    Регистрация нового пользователя с подтверждением почты
    """
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        """
        Проверяет данные на валидность и генерирует случайный ключ
        """
        user = form.save()
        user.is_active = False
        # Генерация случайного ключа
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'https://{host}/users/email-confirm/{token}/'
        send_mail(
            subject="Подтверждение почты",
            message=f"Для подтверждения вашей почты перейдите по ссылке: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    """
    Подтверждение почты с использованием токена
    """

    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class UserResetPasswordView(PasswordResetView, StyleFormMixin):
    """
    Сброс пароля с использованием email
    """
    form_class = ResetPasswordForm
    template_name = 'users/reset_password.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """
        Проверяет валидность и сохраняет новый пароль
        """
        email = form.cleaned_data['email']
        # Проверяем наличие пользователя с указанной почтой
        try:
            user = User.objects.get(email=email)
            if user:
                # Создаем новый пароль для пользователя и отправляем его на почту
                password = ''.join([random.choice(string.digits + string.ascii_letters) for i in range(0, 10)])
                user.set_password(password)
                user.is_active = True
                user.save()
                send_mail(
                    subject='Сброс пароля',
                    message=f'Новый пароль: {password}',
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[user.email]
                )
            return redirect(reverse('users:login'))
        except User.DoesNotExist:
            # Если пользователь не найден, перенаправляем на страницу регистрации
            return redirect(reverse('users:register'))


class ProfileView(UpdateView, StyleFormMixin):
    """
    Отображает и редактирует профиль пользователя
    """
    model = User
    form_class = UserProfileForm
    template_name = 'users/user_profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
