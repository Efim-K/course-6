from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailings.models import Mailings


# Create your views here.
class MailingsListView(ListView):
    """
    Выводит список всех рассылок
    """
    model = Mailings


class MailingsDetailView(DetailView):
    """
    Выводит детальную информацию о рассылке
    """
    model = Mailings


class MailingsCreateView(CreateView):
    model = Mailings
    """
    Создает новую рассылку
    """
    fields = ('launch_at', 'completed_at', 'periodicity', 'status', 'message', 'email_client', 'is_active')
    success_url = reverse_lazy('mailings:mailings_list')


class MailingsUpdateView(UpdateView):
    """
    Редактирует существующую рассылку
    """
    model = Mailings
    fields = ('launch_at', 'completed_at', 'periodicity', 'status', 'message', 'email_client', 'is_active')
    success_url = reverse_lazy('mailings:mailings_list')

    def get_success_url(self):
        return reverse_lazy('mailings:mailings_view', args=[self.object.pk])


class MailingsDeleteView(DeleteView):
    """
    Удаляет существующую рассылку
    """
    model = Mailings
    success_url = reverse_lazy('mailings:mailings_list')
