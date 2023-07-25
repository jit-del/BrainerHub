from django.db import models

# Create your models here.

class Company(models.Model):
    company_name = models.CharField(max_length=100)
    def __str__(self):
        return self.company_name

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    salary = models.IntegerField()
    manager_id = models.IntegerField()
    department_id = models.IntegerField()
 
    def __str__(self):
        return f"{self.first_name} {self.last_name}"