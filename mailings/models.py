from django.db import models

NULLABLE = {"blank": "True", "null": "True"}


class EmailClient(models.Model):
    """ данные для рассылки """

    client_name = models.CharField(max_length=255, verbose_name='Ф. И. О.')
    email = models.EmailField(verbose_name='Email получателя')
    comment = models.TextField(verbose_name='Комментарий к клиенту', **NULLABLE)

    def __str__(self):
        return f'{self.client_name} {self.email}'

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'


class Message(models.Model):
    """ данные для отправки сообщений """

    message_title = models.CharField(max_length=255, verbose_name='Тема сообщения')
    message_text = models.TextField(verbose_name='Текст сообщения')

    def __str__(self):
        return self.message_title

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


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
        ('YEARLY', 'Ежегодно'),
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
    email_client = models.ForeignKey(EmailClient, on_delete=models.CASCADE, verbose_name='Список клиентов')

    def __str__(self):
        return f'Рассылка: {self.pk}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
