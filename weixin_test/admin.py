from django.contrib import admin

from .models import Patient, Doctors

admin.site.register(Patient)
admin.site.register(Doctors)
