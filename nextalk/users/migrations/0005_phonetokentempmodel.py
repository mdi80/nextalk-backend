# Generated by Django 4.2.4 on 2023-08-25 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_user_password_user_userid'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneTokenTempModel',
            fields=[
                ('phone_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('phone', models.CharField(max_length=17)),
            ],
        ),
    ]
