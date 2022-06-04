# Generated by Django 4.0.4 on 2022-05-30 16:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AOHI_admin', '0005_alter_orphans_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestAdoption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('orphan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='request_orphan', to='AOHI_admin.orphans')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='request_acct', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Request Adoption',
                'db_table': 'Request Adoption',
            },
        ),
    ]