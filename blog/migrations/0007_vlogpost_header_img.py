# Generated by Django 2.2.14 on 2020-07-26 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20200726_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='vlogpost',
            name='header_img',
            field=models.ImageField(blank=True, null=True, upload_to='vlog_uploads'),
        ),
    ]
