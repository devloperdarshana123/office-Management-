from django.db import models
from django.utils import timezone

# Department Model
class Department(models.Model):
    name = models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Role Model
class Role(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name

# Employee Model
class Employee(models.Model):
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    salary = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    phone = models.CharField(max_length=15, default="")
    hire_date = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.phone}"

# Attendance Model (Fixed Indentation & Placement)
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(
        max_length=10,
        choices=[("Present", "Present"), ("Absent", "Absent")]
    )

    def __str__(self):
        return f"{self.employee.first_name} - {self.status} on {self.date}"

# Performance Model (Now Correctly Placed)
class Performance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1-5 scale
    feedback = models.TextField()
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.employee.first_name} - {self.rating} Stars"
