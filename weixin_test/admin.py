from django.contrib import admin

from .models import Patient, Doctor

admin.site.register(Patient)
admin.site.register(Doctor)
