# Generated by Django 4.2.4 on 2023-09-11 20:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FileField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachedType', models.IntegerField(choices=[(1, 'file'), (2, 'music'), (3, 'image'), (4, 'video')], default=1)),
                ('FileField', models.FileField(upload_to='chatfiles')),
                ('size', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ChatModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(blank=True, max_length=10000)),
                ('send_date', models.DateTimeField(auto_now_add=True)),
                ('received', models.BooleanField(default=False)),
                ('received_date', models.DateTimeField(blank=True)),
                ('seen', models.BooleanField(default=False)),
                ('seen_date', models.DateTimeField(blank=True)),
                ('attachedFile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.filefield')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='from_user', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
