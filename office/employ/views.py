
from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse
from django.utils import timezone
from .models import Employee, Department, Role  # Ensure these imports are correct
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

def add_emp(request):
    if request.method == 'POST':
        try:
            # Extract data from the form
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            
            # Safely convert to integers only if values are present
            salary = request.POST.get('salary', '0').strip()
            bonus = request.POST.get('bonus', '0').strip()
            phone = request.POST.get('phone', '0').strip()
            
            # Convert to integers with a check to avoid ValueError
            salary = int(salary) if salary.isdigit() else 0
            bonus = int(bonus) if bonus.isdigit() else 0
            phone = int(phone) if phone.isdigit() else 0

            hire_date = request.POST.get('hire_date', '').strip()
            if not hire_date:
                hire_date = timezone.now().date()

            # Fetch Foreign Key objects by name instead of ID
            dept_name = request.POST.get('department', '').strip()
            role_name = request.POST.get('role', '').strip()

            # 🔍 Debug Print: Print the received names
            print(f"Department Name Received: '{dept_name}'")
            print(f"Role Name Received: '{role_name}'")

            # 🔍 Debug Print: Print available names in the database
            available_depts = Department.objects.values_list('name', flat=True)
            available_roles = Role.objects.values_list('name', flat=True)
            print(f"Available Departments: {list(available_depts)}")
            print(f"Available Roles: {list(available_roles)}")

            # Handle missing values
            if not dept_name or not role_name:
                return HttpResponse("Department and Role are required.")

            # Fetch by name (case-insensitive)
            dept = get_object_or_404(Department, Q(name__iexact=dept_name))
            role = get_object_or_404(Role, Q(name__iexact=role_name))

            # Create a new Employee instance
            new_employee = Employee(
                first_name=first_name,
                last_name=last_name,
                salary=salary,
                bonus=bonus,
                phone=phone,
                dept=dept,
                role=role,
                hire_date=hire_date
            )
            new_employee.save()
            return HttpResponse("Employee added successfully!")

        except ValueError as e:
            return HttpResponse(f"Invalid data type provided: {str(e)}")
        except ObjectDoesNotExist:
            return HttpResponse("Invalid department or role name.")
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}")

    elif request.method == "GET":
        return render(request, 'add_emp.html')
    else:
        return HttpResponse("An exception occurred! Employee has not been added.")

def index(request):
    return render(request, 'index.html') 

def all_emp(request):
    employees = Employee.objects.all()
    for emp in employees:
        print(emp.first_name, emp.phone)  # Debug: Print phone numbers in console

    context = {
        'employees': employees
    }
    return render(request, 'all_emp.html', context)





# def remove_emp(request):
#     emps = Employee.objects.all()
#     context = {
#         'emps' = emps
#     }
def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            # Fetch and delete the employee by ID
            emp_to_be_removed = get_object_or_404(Employee, id=emp_id)
            emp_to_be_removed.delete()
            return redirect('remove_emp')
        except Exception as e:
            return HttpResponse(f"An error occurred! Employee has not been removed. Error: {str(e)}")
    
    # Fetch all employees if no ID is provided
    emps = Employee.objects.all()
    return render(request, 'remove_emp.html', {'emps': emps})

    
    
    
    # return render(request, 'remove_emp.html') 
def filter_emp(request):
    if request.method == "POST":
        # Capture form data
        name = request.POST.get('name', '').strip()
        dept = request.POST.get('dept', '').strip()
        role = request.POST.get('role', '').strip()

        # Get all employees initially
        emps = Employee.objects.all()

        # Filter by first or last name (even single character)
        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        
        # Filter by department if provided
        if dept:
            emps = emps.filter(dept__name__icontains=dept)
        
        # Filter by role if provided
        if role:
            emps = emps.filter(role__name__icontains=role)
        
        # Debug prints to check filtering
        print("Name filter:", name)
        print("Dept filter:", dept)
        print("Role filter:", role)
        print("Filtered Employees Count:", emps.count())
        for emp in emps:
            print(f"Employee: {emp.first_name} {emp.last_name}, Dept: {emp.dept.name}, Role: {emp.role.name}")

        # Pass the filters back to the template to keep input fields filled
        context = {
            'emps': emps,
            'name': name,
            'dept': dept,
            'role': role
        }
        return render(request, 'filter_emp.html', context)

    # Handle GET request - display form without results
    return render(request, 'filter_emp.html', {'emps': [], 'name': '', 'dept': '', 'role': ''})