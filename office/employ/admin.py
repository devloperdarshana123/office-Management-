from django.contrib import admin
from .models import Employee , Role , Department
admin.site.register(Department)
admin.site.register(Role)
admin.site.register(Employee)
# Register your models here.
