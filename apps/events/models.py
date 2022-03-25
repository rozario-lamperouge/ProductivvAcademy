from django.db import models
from datetime import datetime
from organizations.models import CourseOrg, Teacher
from django.contrib.auth import get_user_model


User = get_user_model()


# Event Information Form
class Event(models.Model):
    degree_choices = (
        ('elementary', 'primary'),
        ('intermediate', 'intermediate'),
        ('advanced', 'advanced'),
    )
    mode_choices = (
    	('elementary','online'),
    	('intermediate','offline'),
    	)
    # null=True, blank=True Because there is no value in this field
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE,
                                   verbose_name=u'Event organization', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u'Event name')
    desc = models.CharField(max_length=300, verbose_name=u'Event Description')
    detail = models.TextField(verbose_name=u'Event details')
    degree = models.CharField(choices=degree_choices, max_length=15,
                              verbose_name=u'grade')
    mode = models.CharField(choices=mode_choices, max_length=15,
                              verbose_name=u'mode')
    event_time = models.IntegerField(default=0, verbose_name=u'Duration of Event')
    students = models.IntegerField(default=0, verbose_name=u'Number of learners')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,
                                verbose_name=u'teacher', null=True, blank=True)
    category = models.CharField(default=u"Back-end development", max_length=20,
                                verbose_name=u'Event category')
    # Tags to recommend courses based on common tags
    tag = models.CharField(default="", verbose_name=u"Event tags", max_length=30)
    click_nums = models.IntegerField(default=0, verbose_name=u'Clicks')
    # course notes
    event_banner = models.CharField(default='', max_length=400, verbose_name=u'Event Banner')
    # teacher tells you
    whatsapp_link = models.CharField(default='', max_length=400, verbose_name=u'whatsapp-link')

    # whether it is a carousel
    is_banner = models.BooleanField(default=False,verbose_name=u'whether_to_rotate')

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'add_time')
    event_date = models.DateTimeField(default=datetime.now)
    price = models.IntegerField(default=0, verbose_name=u'event price')

    class Meta:
        verbose_name = u'Event'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name