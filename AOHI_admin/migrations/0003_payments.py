# Generated by Django 4.0.4 on 2022-05-28 17:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AOHI_admin', '0002_adoptions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('adopted_date', models.DateTimeField(auto_now_add=True)),
                ('date_paid', models.DateTimeField(auto_now_add=True)),
                ('orphan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orphan_payment', to='AOHI_admin.orphans')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_paid_acct', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Payments',
                'db_table': 'Payments',
            },
        ),
    ]