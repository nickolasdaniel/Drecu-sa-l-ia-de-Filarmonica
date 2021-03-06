# Generated by Django 2.1.3 on 2019-02-28 10:29

import account.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilaUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('email2', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('first_name', models.CharField(max_length=25, null=True)),
                ('last_name', models.CharField(max_length=30, null=True)),
                ('password', models.CharField(max_length=99)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'users',
                'abstract': False,
                'verbose_name': 'user',
            },
            managers=[
                ('objects', account.models.FilaManager()),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(help_text='Select the day of the event', verbose_name='Day of the event')),
            ],
            options={
                'verbose_name_plural': 'Scheduling',
                'verbose_name': 'Scheduling',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('last_name', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('phone', models.IntegerField(blank=True, null=True)),
                ('instagram', models.URLField(blank=True, max_length=199, null=True)),
                ('facebook', models.URLField(blank=True, max_length=199, null=True)),
                ('caption', models.CharField(blank=True, max_length=2500, null=True)),
                ('filauser', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('first_name', 'last_name'),
            },
        ),
    ]
