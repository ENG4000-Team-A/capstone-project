from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStamp(models.Model):
    hours = models.PositiveIntegerField(default=0)
    # Use Validators to restrict minutes and seconds to [1, 60]. ValidationError will be raised if not within the range
    minutes = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(60)], default=0)
    seconds = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(60)], default=0)
