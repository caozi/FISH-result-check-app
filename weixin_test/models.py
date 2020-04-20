from django.db import models


class Patient(models.Model):
    patient_id = models.CharField(unique=True, max_length=200)
    patient_name = models.CharField(max_length=200)
    patient_openID = models.CharField(max_length=200)
    patient_status = models.CharField(max_length=200)

    def __str__(self):
        return self.patient_id


class Doctors(models.Model):
    doctor_name = models.CharField(max_length=200)
    doctor_password = models.CharField(max_length=200)

    def __str__(self):
        return self.doctor_name
