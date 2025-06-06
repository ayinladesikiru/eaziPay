# Generated by Django 5.2 on 2025-04-14 10:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='transaction_time',
            new_name='transaction_date',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='name',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='wallet',
        ),
        migrations.AddField(
            model_name='transaction',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('D', 'DEPOSIT'), ('W', 'WITHDRAW'), ('T', 'TRANSFER')], default='D', max_length=1),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='receiver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='reference',
            field=models.CharField(max_length=40, unique=True),
        ),
    ]
