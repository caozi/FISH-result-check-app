from django.contrib import admin

from .models import Patient, Doctors, Member

admin.site.register(Patient)
admin.site.register(Doctors)
admin.site.register(Member)
