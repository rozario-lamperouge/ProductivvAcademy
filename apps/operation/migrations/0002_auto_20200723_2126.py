# Generated by Django 2.0.12 on 2020-07-23 21:26

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coursecomments',
            options={'verbose_name': 'courseTitle', 'verbose_name_plural': 'courseTitle'},
        ),
        migrations.AlterModelOptions(
            name='userask',
            options={'verbose_name': 'userConsultation', 'verbose_name_plural': 'userConsultation'},
        ),
        migrations.AlterModelOptions(
            name='usercourse',
            options={'verbose_name': 'userCourse', 'verbose_name_plural': 'userCourse'},
        ),
        migrations.AlterModelOptions(
            name='userfavorite',
            options={'verbose_name': 'userFavorites', 'verbose_name_plural': 'userFavorites'},
        ),
        migrations.AlterModelOptions(
            name='usermessage',
            options={'verbose_name': 'userMessage', 'verbose_name_plural': 'userMessage'},
        ),
        migrations.AlterField(
            model_name='coursecomments',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='commentTime'),
        ),
        migrations.AlterField(
            model_name='coursecomments',
            name='comments',
            field=models.CharField(max_length=250, verbose_name='comment'),
        ),
        migrations.AlterField(
            model_name='coursecomments',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='course'),
        ),
        migrations.AlterField(
            model_name='coursecomments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='userask',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='addTime'),
        ),
        migrations.AlterField(
            model_name='userask',
            name='course_name',
            field=models.CharField(max_length=50, verbose_name='courseName'),
        ),
        migrations.AlterField(
            model_name='userask',
            name='mobile',
            field=models.CharField(max_length=11, verbose_name='cellularPhone'),
        ),
        migrations.AlterField(
            model_name='userask',
            name='name',
            field=models.CharField(max_length=20, verbose_name='fullName'),
        ),
        migrations.AlterField(
            model_name='usercourse',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='addTime'),
        ),
        migrations.AlterField(
            model_name='usercourse',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='course'),
        ),
        migrations.AlterField(
            model_name='usercourse',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='userfavorite',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='commentTime'),
        ),
        migrations.AlterField(
            model_name='userfavorite',
            name='fav_type',
            field=models.IntegerField(choices=[(1, 'course'), (2, 'courseOrganization'), (3, 'instructor')], default=1, verbose_name='Collection type'),
        ),
        migrations.AlterField(
            model_name='userfavorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='usermessage',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='addTime'),
        ),
        migrations.AlterField(
            model_name='usermessage',
            name='has_read',
            field=models.BooleanField(default=False, verbose_name='haveRead'),
        ),
        migrations.AlterField(
            model_name='usermessage',
            name='message',
            field=models.CharField(max_length=500, verbose_name='messageContent'),
        ),
        migrations.AlterField(
            model_name='usermessage',
            name='user',
            field=models.IntegerField(default=0, verbose_name='receivingUser'),
        ),
    ]
