# Generated by Django 2.0.4 on 2018-07-19 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p_ems', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='userguide',
            field=models.FileField(blank=True, null=True, upload_to='Equipment/UserGuide/%Y%m%d/', verbose_name='用户手册'),
        ),
    ]