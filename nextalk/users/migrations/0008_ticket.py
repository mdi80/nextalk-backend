# Generated by Django 4.2.4 on 2023-09-07 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('knox', '0008_remove_authtoken_salt'),
        ('users', '0007_delete_phonetokentempmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticket', models.CharField(max_length=17, primary_key=True, serialize=False)),
                ('ip', models.GenericIPAddressField()),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knox.authtoken')),
            ],
        ),
    ]
