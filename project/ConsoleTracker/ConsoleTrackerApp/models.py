from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class TimeStamp(models.Model):
    hours = models.PositiveIntegerField(default=0)
    # Use Validators to restrict minutes and seconds to [1, 60]. ValidationError will be raised if not within the range
    minutes = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(60)], default=0)
    seconds = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(60)], default=0)


class Machine(models.Model):
    name = models.TextField(blank=True, null=False)
    active = models.BooleanField(default=False)
    ip = models.GenericIPAddressField(default="127.0.0.1", null=False, unique=True)
    # TODO (Future User Model will be mapped to a machine
    # user = models.OneToOneField(
    #     User,
    #     on_delete=models.CASCADE,
    #     foreign_key=True,
    # )


class User(models.Model):
    name = models.TextField(blank=True, null=False)
    time = models.IntegerField(default=0)


class User_uses_machine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(default=timezone.now)
    expired = models.BooleanField(default=False, null=False) 

    # changes to these values are not respected on django-admin
    readonly_fields=('expired','end_time', 'start_time')
    

# only way to set end_time based on a Users time field
# only runs on object creation 
@receiver(post_save, sender=User_uses_machine)
def calc_end_time(sender, instance,created, **kwargs):
    if created:
        instance.end_time = instance.start_time + timezone.timedelta(seconds=instance.user.time)
        instance.save()


