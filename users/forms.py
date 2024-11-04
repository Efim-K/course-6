from django import forms
from django.contrib.auth.forms import (PasswordResetForm, UserChangeForm,
                                       UserCreationForm)

from users.models import User


class StyleFormMixin:
    """
    Mixin для стилизации формы.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class UserRegisterForm(UserCreationForm, StyleFormMixin):
    """Форма регистрации пользователя"""

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class ResetPasswordForm(PasswordResetForm, StyleFormMixin):
    """Форма для сброса пароля"""

    class Meta:
        model = User
        fields = [
            "email",
        ]


class UserProfileForm(UserChangeForm, StyleFormMixin):
    """Форма редактирования профиля пользователя"""

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone",
            "avatar",
            "country",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.HiddenInput()
