# Generated by Django 2.0.12 on 2022-03-05 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0015_auto_20211207_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='checksum',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
