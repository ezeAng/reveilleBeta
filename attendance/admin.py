from django.contrib import admin
from .models import Personnel, Parade, Absence, Status

admin.site.register(Personnel)
admin.site.register(Parade)
admin.site.register(Absence)
admin.site.register(Status)
