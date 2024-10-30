from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from mailings.forms import MailingsForm, MailingsModeratorForm
from mailings.models import Mailings, Message, EmailClient


# Create your views here.
class MailingsListView(ListView):
    """
    Выводит список всех рассылок
    """
    model = Mailings

    def get_queryset(self):
        """
        Выводит только рассылки текущего пользователя или без автора
        """
        user = self.request.user
        if not user.is_authenticated:
            return Mailings.objects.filter(owner=None)
        if user.has_perm('mailings.change_active_mailing'):
            return Mailings.objects.all()
        return Mailings.objects.filter(owner=user) | Mailings.objects.filter(owner=None)


class MailingsDetailView(LoginRequiredMixin, DetailView):
    """
    Выводит детальную информацию о рассылке
    """
    model = Mailings


class MailingsCreateView(LoginRequiredMixin, CreateView):
    model = Mailings
    """
    Создает новую рассылку
    """
    fields = ('launch_at', 'completed_at', 'periodicity', 'message', 'email_client', 'is_active')
    success_url = reverse_lazy('mailings:mailings_list')

    def form_valid(self, form):
        """
        Сохраняет новую рассылку и связывает ее с текущим пользователем
        """
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class MailingsUpdateView(LoginRequiredMixin, UpdateView):
    """
    Редактирует существующую рассылку
    """
    model = Mailings
    form_class = MailingsForm
    fields = ('launch_at', 'completed_at', 'periodicity', 'status', 'message', 'email_client', 'is_active')
    success_url = reverse_lazy('mailings:mailings_list')

    def get_success_url(self):
        """ Возвращает URL, на который перенаправляется после успешного сохранения """
        return reverse_lazy('mailings:mailings_view', args=[self.object.pk])

    def get_form_class(self):
        """ Получаем форму в зависимости от прав пользователя  """
        user = self.request.user
        if user == self.object.owner:
            return MailingsForm
        if user.has_perm('mailings.change_active_mailing'):
            return MailingsModeratorForm
        raise PermissionDenied('У вас недостаточно прав для редактирования.')

    def form_valid(self, form):

        mailings = form.save()
        mailings.user = self.request.user
        mailings.save()
        return super().form_valid(form)


class MailingsDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаляет существующую рассылку
    """
    model = Mailings
    success_url = reverse_lazy('mailings:mailings_list')


class MessageListView(ListView):
    """
    Выводит список всех сообщений
    """
    model = Message

    def get_queryset(self):
        """
        Выводит только сообщения текущего пользователя или без автора
        """
        user = self.request.user
        if not user.is_authenticated:
            return Message.objects.filter(owner=None)
        if user.has_perm('mailings.change_active_mailing'):
            return Message.objects.all()
        return Message.objects.filter(owner=user) | Message.objects.filter(owner=None)

class MessageDetailView(LoginRequiredMixin, DetailView):
    """
    Выводит детальную информацию о сообщении
    """
    model = Message
    template_name = 'mailings/message_detail.html'


class MessageCreateView(LoginRequiredMixin, CreateView):
    """
    Создает новое сообщение
    """
    model = Message
    fields = ('message_title', 'message_text',)
    success_url = reverse_lazy('mailings:message_list')

    def form_valid(self, form):
        """
        Сохраняет новое сообщение и связывает его с текущим пользователем
        """
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """
    Редактирует существующее сообщение
    """
    model = Message
    fields = ('message_title', 'message_text',)
    success_url = reverse_lazy('mailings:message_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаляет существующее сообщение
    """
    model = Message
    success_url = reverse_lazy('mailings:message_list')


class EmailClientListView(ListView):
    """
    Выводит список всех клиентов почты
    """
    model = EmailClient

    def get_queryset(self):
        """
        Выводит только клиентов текущего пользователя или без автора
        """
        user = self.request.user
        if not user.is_authenticated:
            return EmailClient.objects.filter(owner=None)
        if user.has_perm('mailings.change_active_mailing'):
            return EmailClient.objects.all()
        return EmailClient.objects.filter(owner=user) | EmailClient.objects.filter(owner=None)

class EmailClientCreateView(LoginRequiredMixin, CreateView):
    """
    Создает нового клиента почты
    """
    model = EmailClient
    fields = ('name', 'email', 'comment',)
    success_url = reverse_lazy('mailings:emailclient_list')

    def form_valid(self, form):
        """
        Сохраняет нового клиента почты и связывает его с текущим пользователем
        """
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class EmailClientUpdateView(LoginRequiredMixin, UpdateView):
    """
    Редактирует существующего клиента почты
    """
    model = EmailClient
    fields = ('name', 'email', 'comment',)
    success_url = reverse_lazy('mailings:emailclient_list')


class EmailClientDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаляет существующего клиента почты
    """
    model = EmailClient
    success_url = reverse_lazy('mailings:emailclient_list')
