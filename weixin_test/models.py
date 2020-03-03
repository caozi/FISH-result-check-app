from django.db import models


class Result(models.Model):
    result = models.CharField(max_length=200)

    def __str__(self):
        return self.result

class Patient(models.Model):
    patient_id = models.CharField(unique=True,max_length=200)
    patient_name = models.CharField(max_length=200)
    patient_gender = models.CharField(max_length=200)
    patient_age = models.IntegerField()
    patient_openID = models.CharField(max_length=200)
    patient_result = models.ForeignKey(Result,on_delete=models.CASCADE,blank=True)

    def __str__(self):
        return self.patient_id












