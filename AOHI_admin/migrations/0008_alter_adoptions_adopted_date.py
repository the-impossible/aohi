# Generated by Django 4.0.4 on 2022-06-03 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AOHI_admin', '0007_requestadoption_adopted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adoptions',
            name='adopted_date',
            field=models.DateField(auto_now=True),
        ),
    ]
