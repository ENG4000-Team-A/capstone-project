from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

'''
    TimeStamp (Model)
        - hours = positive integer field
            - default = 0
        - minutes = integer field
            - default = 0
            - range [0, 60]
        - seconds = integer field
            - default = 0
            - range [0, 60]
'''


class TimeStamp(models.Model):
    hours = models.PositiveIntegerField(default=0)
    # Use Validators to restrict minutes and seconds to [1, 60]. ValidationError will be raised if not within the range
    minutes = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(60)], default=0)
    seconds = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(60)], default=0)


'''
    Machine (Model)
        - name = text field
            - default = ''
        - active = boolean field
            - default = false
        - ip = generic ip address field
            - default = "127.0.0.1"
            - unique = true
'''


class Machine(models.Model):
    name = models.TextField(blank=True, null=False)
    active = models.BooleanField(default=False)
    ip = models.GenericIPAddressField(default="127.0.0.1", null=False, unique=True)


'''
    User (Model)
        - username = text field
            - default = ''
        - first_name = text field
            - default = ''
        - last_name = text field
            - default = ''
        - time = integer field
            - default = 0
        - phone_number = char field
            - default = ''
'''


class User(models.Model):
    username = models.TextField(blank=True, null=False, unique=True)
    first_name = models.TextField(blank=True, null=False)
    last_name = models.TextField(blank=True, null=False)
    time = models.PositiveIntegerField(default=0, null=False)
    phone_number = models.CharField(max_length=12, blank=True, null=False)


'''
    User_uses_machine (Relationship Model)
        - user = foreign key field
            - maps to User (Model)
        - machine = foreign key field
            -  maps to Machine (Model)
        - start_time = date time field model
            - default = time now
            - readonly = true
        - end_time = date time field model
            - default = time now in timezone
            - readonly = true
        - expired = boolean field
            - default = false
            - readonly = true
'''


class User_uses_machine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    expired = models.BooleanField(default=False, null=False)

    # changes to these values are not respected on django-admin
    readonly_fields = ('expired', 'end_time', 'start_time')


# only way to set end_time based on a Users time field
@receiver(post_save, sender=User_uses_machine)
def on_creation_uses(sender, instance, created, **kwargs):
    if created:
        instance.machine.active = True
        instance.machine.save()

        instance.end_time = instance.start_time + timezone.timedelta(seconds=instance.user.time)
        instance.save()
