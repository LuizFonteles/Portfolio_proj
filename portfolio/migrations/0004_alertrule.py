# Generated by Django 5.2 on 2025-05-05 22:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_alter_stocks_followed_high_alter_stocks_followed_low_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlertRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('threshold', models.FloatField(help_text='Notify when price falls below this')),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('followed_stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alert_rules', to='portfolio.stocks_followed')),
            ],
        ),
    ]
