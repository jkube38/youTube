# Generated by Django 3.2.8 on 2021-11-02 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youTube_app', '0002_downloaduser_user_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='downloaduser',
            name='user_pic',
            field=models.FileField(blank=True, null=True, upload_to='images/'),
        ),
    ]
