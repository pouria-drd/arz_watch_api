# Generated by Django 5.2 on 2025-04-23 08:55

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_id', models.BigIntegerField(unique=True)),
                ('username', models.CharField(blank=True, max_length=150, null=True)),
                ('first_name', models.CharField(blank=True, max_length=150, null=True)),
                ('last_name', models.CharField(blank=True, max_length=150, null=True)),
                ('is_bot', models.BooleanField(default=False)),
                ('is_premium', models.BooleanField(default=False)),
                ('language_code', models.CharField(blank=True, max_length=10, null=True)),
                ('request_count', models.PositiveIntegerField(default=0)),
                ('max_requests', models.PositiveIntegerField(default=100)),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('banned', 'Banned'), ('inactive', 'Inactive')], default='active', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_seen', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_reset_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Telegram User',
                'verbose_name_plural': 'Telegram Users',
                'indexes': [models.Index(fields=['user_id'], name='telegram_te_user_id_8111fa_idx'), models.Index(fields=['username'], name='telegram_te_usernam_cc492e_idx'), models.Index(fields=['is_active'], name='telegram_te_is_acti_cf4848_idx'), models.Index(fields=['last_seen'], name='telegram_te_last_se_b29bb2_idx'), models.Index(fields=['last_reset_at'], name='telegram_te_last_re_b1036d_idx')],
            },
        ),
        migrations.CreateModel(
            name='TelegramCommand',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('command_type', models.CharField(choices=[('coin', 'Coin'), ('gold', 'Gold'), ('crypto', 'Crypto'), ('currency', 'Currency')], db_index=True, max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('tg_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='commands', to='telegram.telegramuser')),
            ],
            options={
                'verbose_name': 'Telegram Command',
                'verbose_name_plural': 'Telegram Commands',
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['tg_user'], name='telegram_te_tg_user_2c8ec7_idx'), models.Index(fields=['command_type'], name='telegram_te_command_058905_idx'), models.Index(fields=['created_at'], name='telegram_te_created_457916_idx')],
            },
        ),
    ]
