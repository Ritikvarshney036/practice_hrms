from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    emp_id = models.CharField(max_length=10, unique=True)
    department = models.CharField(max_length=50)
    email = models.EmailField()
    join_date = models.DateField()

    def __str__(self):
        return self.name
