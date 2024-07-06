# Generated by Django 4.2 on 2024-07-06 10:33

from django.db import migrations, models
import phonenumber_field.modelfields
import user.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organisation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('userId', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('firstName', models.CharField(max_length=255)),
                ('lastName', models.CharField(max_length=255)),
                ('email', models.EmailField(error_messages={'unique': 'User with email already exists'}, max_length=254, unique=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='NG')),
                ('organisations', models.ManyToManyField(blank=True, to='organisation.organisation')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', user.managers.UserManager()),
            ],
        ),
    ]
