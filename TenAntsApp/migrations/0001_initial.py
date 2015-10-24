# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HousingPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('bedrooms', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('bathrooms', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('rating', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(10.0)])),
                ('longitude', models.FloatField(null=True)),
                ('latitude', models.FloatField(null=True)),
                ('line1', models.CharField(max_length=95, null=True)),
                ('line2', models.CharField(max_length=95, null=True)),
                ('city', models.CharField(max_length=35, null=True)),
                ('zip_code', models.CharField(max_length=16, null=True)),
                ('property_name', models.CharField(max_length=64, null=True)),
                ('title', models.CharField(max_length=64)),
                ('last_updated', models.DateField()),
                ('state_date', models.DateField()),
                ('end_date', models.DateField()),
                ('description', models.CharField(max_length=2048, null=True)),
                ('num_people', models.PositiveIntegerField(null=True, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'')),
                ('housing_post', models.ForeignKey(to='TenAntsApp.HousingPost')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=2048)),
                ('satisfaciton_rating', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('safety_rating', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('housing_post', models.ForeignKey(to='TenAntsApp.HousingPost')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
