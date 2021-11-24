from django.contrib import admin
from .models import TimeStamp, Machine, User, User_uses_machine

admin.site.register(TimeStamp)
admin.site.register(Machine)
admin.site.register(User)
admin.site.register(User_uses_machine)

