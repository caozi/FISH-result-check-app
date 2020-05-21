from django.db import models


#医生
class Doctor(models.Model):
    doctor_openID = models.CharField(unique=True, max_length=100)
    doctor_name = models.CharField(max_length=20)

    def __str__(self):
        return self.doctor_name


#患者
class Patient(models.Model):
    patient_id = models.CharField(unique=True, max_length=10)
    patient_name = models.CharField(max_length=50)
    patient_openID = models.CharField(max_length=100)
    patient_phone = models.CharField(max_length=11)
    patient_status = models.CharField(max_length=50)
    patient_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient_note = models.CharField(max_length=200)

    def __str__(self):
        return self.patient_id



