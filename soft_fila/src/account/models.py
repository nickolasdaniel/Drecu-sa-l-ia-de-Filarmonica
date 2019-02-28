import pytz
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser,BaseUserManager,User
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import datetime
"""
class FilaSub(models.Model):

    email = models.EmailField(_('Email'),unique=True)
    creation_date = models.DateTimeField(_('Membru de la data'),default=now())

    class Meta:

        verbose_name  = "Fila"
        verbose_name_plural = "Fila"

    def __str__(self):

        return "{}" .format(self.email)
"""
class FilaManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError("Email must be passed")

        email = self.normalize_email(email)

        user = self.model(email = email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email,password=None, **extra_fields):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email,password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(email,password, **extra_fields)


class FilaUser(AbstractUser):

    username = None
    email = models.EmailField(_('Email'),unique=True)
    email2 = models.EmailField(_('Email'),unique=True)

    first_name = models.CharField(max_length=25, blank=False, null=True)
    last_name = models.CharField(max_length=30, blank=False, null=True)
    password = models.CharField(max_length=99,blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = FilaManager()

    def __str__(self):

        return self.email

class Profile(models.Model):

    filauser = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='userprofile')

    first_name = models.CharField(max_length=20,unique=True,null=True,blank=True)
    last_name = models.CharField(max_length=20,unique=True,null=True,blank=True)

    photo = models.ImageField(upload_to='images/',blank=True,null=True)
    phone = models.IntegerField(blank=True,null=True)

    instagram = models.URLField(max_length=199,null=True,blank=True)
    facebook = models.URLField(max_length=199,null=True,blank=True)

    caption = models.CharField(max_length=2500,blank=True,null=True)

    def __str__(self):
        return '{} {}'.format(self.filauser.first_name,self.filauser.last_name)

    class Meta:
        ordering = ('first_name','last_name',)

    """@receiver(post_save,sender = FilaUser)
    def create_user_profile(sender,instance,created,**kwargs):

        if created:
            profile = Profile.objects.create(filauser = instance)
            profile.post_save()
    """
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(filauser = instance)

post_save.connect(create_user_profile,sender=FilaUser)

class Events(models.Model):

    UserEvent = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete = models.CASCADE,related_name ='user_event')

    day = models.DateField(u'Day of the event',help_text="Select the day of the event",default='2001-02-01')
    concert_type = models.CharField(u'Type of concert',max_length=100,help_text='Select the type of concert',default='vocal-simfonic')
    vocal_type = models.CharField(u'Type of vocalist',max_length=100,help_text='Select the vocalist type',default='mezzosopran')
    city = models.CharField(u'City',max_length=100,help_text='Select the city',default='Timisoara')
    location = models.CharField(u'Location',max_length=100,help_text='Select the city location',default='Capitol')
    room = models.CharField(u'room',max_length=100,help_text='Select the location room',default='')

    start_time = models.TimeField(u'Starting Time',help_text='Select the time to start the event',default=datetime.time(hour=8))
    final_time = models.TimeField(u'Final Time',help_text='Select the time to end the event',default=datetime.time(hour=9))

    def check_overlap(self,fixed_start,fixed_end,new_start,new_end):

        overlap = False

        if new_start == fixed_end or new_end == fixed_start:
            overlap = False

        elif (new_start >= fixed_start and new_start <= fixed_end) or (new_end >= fixed_start and new_end <=fixed_end):
            overlap = True

        elif new_start <= fixed_start and new_end >= fixed_end:
            overlap = True

        return overlap

    def clean(self):

        if self.final_time <= self.start_time:
            raise ValidationError('Ending times must after starting times')

        events = Events.objects.filter(day = self.day).values_list('start_time',flat=True)
        if events.exists():
            for event in events:
                if self.check_overlap(event.start_time,event.end_time,self.start_time,self.final_time):
                    raise ValidationError('There is an overlap with another event: ' + str(event.day) + ', ' + str(event.start_time) + '-' + str(event.end_time))

    def __str__(self):
        return '{} {}'.format(self.day,self.UserEvent)

    class Meta:

        verbose_name = u'Scheduling'
        verbose_name_plural = u'Scheduling'
        ordering = ('day',)


def create_user_event(sender,instance,created,**kwargs):
    if created:
        Events.objects.create(UserEvent = instance)

post_save.connect(create_user_event,sender=FilaUser)

"""@receiver(post_save,sender = FilaUser)
    def save_user_profile(sender,instance,**kwargs):

        instance.profile.post_save()
"""
