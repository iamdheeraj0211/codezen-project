# Generated by Django 4.2.5 on 2023-09-09 17:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('productapp', '0004_alter_orders_seller_alter_platformapicall_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platformapicall',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
