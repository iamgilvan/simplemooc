# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-14 19:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0002_auto_20180113_1811'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('content', models.TextField(verbose_name='Content')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create in ')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update in ')),
            ],
            options={
                'ordering': ['-created_at'],
                'verbose_name_plural': 'Announcements',
                'verbose_name': 'Announcement',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.TextField(verbose_name='Comments')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create in ')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update in ')),
                ('announcements', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='courses.Announcement', verbose_name='Announcement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'ordering': ['created_at'],
                'verbose_name_plural': 'Comments',
                'verbose_name': 'Comment',
            },
        ),
        migrations.RenameField(
            model_name='course',
            old_name='create_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='update_at',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='enrollment',
            old_name='create_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='enrollment',
            old_name='update_at',
            new_name='updated_at',
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='status',
            field=models.IntegerField(blank=True, choices=[(0, 'Pendant'), (1, 'Approved'), (2, 'Canceled')], default=0, verbose_name='Situation'),
        ),
        migrations.AddField(
            model_name='announcement',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='course'),
        ),
    ]