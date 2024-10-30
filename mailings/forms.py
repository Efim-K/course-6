from django.forms import ModelForm, BooleanField

from mailings.models import Mailings
from users.forms import StyleFormMixin


class MailingsForm(ModelForm, StyleFormMixin):
    """
    Форма рассылки
    """

    class Meta:
        model = Mailings
        exclude = ('owner', 'status',)


class MailingsModeratorForm(ModelForm, StyleFormMixin):
    """
    Форма модератора для редактирования рассылки
    """

    class Meta:
        model = Mailings
        fields = ('is_active',)
