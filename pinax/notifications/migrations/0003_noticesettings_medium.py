# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-03 10:59
from __future__ import unicode_literals

from django.db import migrations, models


def update_medium_field(apps, schema_editor):
    """Previously mediums were stored as single character IDs (ugh)
    No they are just stored as labels. This works with a single backend configured."""
    from ..utils import load_media_defaults
    media, _ = load_media_defaults()
    NoticeSetting = apps.get_model('pinax_notifications', 'NoticeSetting')
    count = 0
    for setting in NoticeSetting.objects.all():
        setting.medium = media[int(setting.medium)][0]
        setting.save()
        count += 1
    if count:
        print('Updated %s NoticeSettings' %count)



class Migration(migrations.Migration):

    dependencies = [
        ('pinax_notifications', '0002_noticetype_permission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticesetting',
            name='medium',
            field=models.CharField(choices=[('email', 'email')], max_length=100, verbose_name='medium'),
        ),
        migrations.RunPython(update_medium_field)
    ]