# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-09-03 15:47


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hs_communities', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topicentry',
            name='topic',
        ),
        migrations.RemoveField(
            model_name='topics',
            name='topics',
        ),
        migrations.AddField(
            model_name='topic',
            name='order',
            field=models.IntegerField(default=0, help_text=b'Position of this entry: 1-n'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='TopicEntry',
        ),
        migrations.DeleteModel(
            name='Topics',
        ),
    ]
