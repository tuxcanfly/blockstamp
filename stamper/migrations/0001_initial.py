# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-22 00:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WebPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('url', models.URLField()),
                ('address', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Confirmed')], default=0)),
            ],
            options={
                'ordering': ('created',),
                'get_latest_by': 'created',
            },
        ),
    ]
