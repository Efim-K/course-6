from django.db import models

from users.models import User

NULLABLE = {"blank": "True", "null": "True"}


class EmailClient(models.Model):
    """ данные для рассылки """

    name = models.CharField(max_length=255, verbose_name='Ф. И. О.')
    email = models.EmailField(verbose_name='Email получателя')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(User, verbose_name="Владелец", on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f'{self.name} {self.email}'

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'
        ordering = ['owner', 'name', ]


class Message(models.Model):
    """ данные для отправки сообщений """

    message_title = models.CharField(max_length=255, verbose_name='Тема сообщения')
    message_text = models.TextField(verbose_name='Текст сообщения')
    owner = models.ForeignKey(User, verbose_name="Владелец", on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return self.message_title

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['owner', 'message_title', ]


# Create your models here.
class Mailings(models.Model):
    """ данные для рассылок """

    MAILINGS_CHOICES = (
        ('CREATED', 'создана'),
        ('LAUNCHED', 'запущена'),
        ('COMPLETED', 'завершена'),
    )
    MAILINGS_PERIODICITY = (
        ('ONCE', 'Однократно'),
        ('DAILY', 'Ежедневно'),
        ('WEEKLY', 'Еженедельно'),
        ('MONTHLY', 'Ежемесячно'),
    )

    launch_at = models.DateTimeField(
        **NULLABLE,
        verbose_name='Дата запуска рассылки'
    )
    completed_at = models.DateTimeField(
        **NULLABLE,
        verbose_name='Дата завершения рассылки'
    )

    periodicity = models.CharField(
        max_length=255,
        choices=MAILINGS_PERIODICITY,
        default='ONCE',
        verbose_name='Периодичность'
    )

    status = models.CharField(
        max_length=255,
        choices=MAILINGS_CHOICES,
        default='CREATED',
        verbose_name='Статус рассылки',
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    email_client = models.ManyToManyField(EmailClient, verbose_name='Получатели')
    is_active = models.BooleanField(default=True, verbose_name='Активная рассылка')

    owner = models.ForeignKey(User, verbose_name="Владелец", on_delete=models.SET_NULL, **NULLABLE)

    def get_email_client(self):
        """ Возвращает список получателей в виде строки """
        return ",".join([str(p) for p in self.email_client.all()])

    def get_revers_active(self):
        """ Возвращает инвертированное состояние активности рассылки """
        try:
            mailings = Mailings.objects.get(pk=self.pk)
            mailings.is_active = not mailings.is_active
            mailings.save()
            return mailings.is_active
        except Mailings.DoesNotExist:
            return 'Рассылки с таким ID не существует!'

    def __str__(self):
        return f'Рассылка: {self.pk}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['owner', 'launch_at', ]
