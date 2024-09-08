# Generated by Django 5.1.1 on 2024-09-08 08:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=255, verbose_name='Ф. И. О.')),
                ('email', models.EmailField(max_length=254, verbose_name='Email получателя')),
                ('comment', models.TextField(blank='True', null='True', verbose_name='Комментарий к клиенту')),
            ],
            options={
                'verbose_name': 'Клиент сервиса',
                'verbose_name_plural': 'Клиенты сервиса',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_title', models.CharField(max_length=255, verbose_name='Тема сообщения')),
                ('message_text', models.TextField(verbose_name='Текст сообщения')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.CreateModel(
            name='Mailings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('launch_at', models.DateTimeField(blank='True', null='True', verbose_name='Дата запуска рассылки')),
                ('completed_at', models.DateTimeField(blank='True', null='True', verbose_name='Дата завершения рассылки')),
                ('periodicity', models.CharField(choices=[('DAILY', 'Ежедневно'), ('WEEKLY', 'Еженедельно'), ('MONTHLY', 'Ежемесячно')], default='MONTHLY', max_length=255, verbose_name='Периодичность')),
                ('status', models.CharField(choices=[('CREATED', 'создана'), ('LAUNCHED', 'запущена'), ('COMPLETED', 'завершена')], default='CREATED', max_length=255, verbose_name='Статус рассылки')),
                ('EmailClient', models.ManyToManyField(to='mailings.emailclient', verbose_name='Список клиентов')),
                ('Message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailings.message', verbose_name='Сообщение')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
            },
        ),
    ]