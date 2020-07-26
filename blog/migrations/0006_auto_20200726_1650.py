# Generated by Django 2.2.14 on 2020-07-26 16:50

from django.db import migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20200725_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vlogpost',
            name='video_url',
            field=embed_video.fields.EmbedVideoField(blank=True, null=True, verbose_name='YouTube Link'),
        ),
    ]
