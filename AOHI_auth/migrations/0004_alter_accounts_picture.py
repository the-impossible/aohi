# Generated by Django 4.0.4 on 2022-05-29 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AOHI_auth', '0003_alter_accounts_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts',
            name='picture',
            field=models.ImageField(default='user.png', null=True, upload_to='uploaded/'),
        ),
    ]