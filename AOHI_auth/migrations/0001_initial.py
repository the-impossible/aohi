# Generated by Django 4.0.4 on 2022-05-28 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('firstname', models.CharField(db_index=True, max_length=30)),
                ('lastname', models.CharField(blank=True, db_index=True, max_length=30)),
                ('phone_number', models.CharField(db_index=True, max_length=14)),
                ('email', models.EmailField(blank=True, db_index=True, max_length=50, unique=True, verbose_name='email address')),
                ('picture', models.ImageField(default='user.png', null=True, upload_to='')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date_joined')),
                ('last_login', models.DateTimeField(auto_now=True, null=True, verbose_name='last_login')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'Accounts',
                'db_table': 'Accounts',
            },
        ),
    ]