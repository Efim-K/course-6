# Generated by Django 5.1.1 on 2024-11-03 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailclient',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email получателя'),
        ),
    ]
