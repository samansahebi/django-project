# Generated by Django 5.1.3 on 2024-11-26 11:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_phonenumber_user_phonenumber_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='customers',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
