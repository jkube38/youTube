# Generated by Django 3.2.8 on 2021-11-06 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youTube_app', '0005_auto_20211103_1650'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemporaryUrl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('snippet', models.CharField(max_length=16)),
                ('user', models.CharField(max_length=30)),
            ],
        ),
    ]