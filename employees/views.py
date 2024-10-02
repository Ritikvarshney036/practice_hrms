from django.shortcuts import render, redirect
from .forms import EmployeeForm

def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()  # Save the employee details to the database
            return redirect('employee_list')  # Redirect to list of employees
    else:
        form = EmployeeForm()
    
    return render(request, 'employees/add_employee.html', {'form': form})

from django.shortcuts import render, get_object_or_404
from .models import Employee

def generate_letter(request):
    if request.method == 'POST':
        emp_id = request.POST.get('emp_id')
        employee = get_object_or_404(Employee, emp_id=emp_id)

        # Prepare context for the resignation letter
        context = {
            'employee_name': employee.name,
            'employee_id': employee.emp_id,
            'resignation_date': 'Today’s Date',  # You can use date.today() for dynamic dates
        }

        return render(request, 'employees/resignation_letter.html', context)

    # If GET request, display form to select employee
    employees = Employee.objects.all()
    return render(request, 'employees/select_employee.html', {'employees': employees})

from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO

def download_pdf(request, emp_id):
    employee = get_object_or_404(Employee, emp_id=emp_id)

    # Prepare context
    context = {
        'employee_name': employee.name,
        'employee_id': employee.emp_id,
        'resignation_date': 'Today’s Date',
    }

    # Render the resignation letter HTML template
    template_name = 'employees/resignation_letter.html'
    html = render(request, template_name, context).content.decode('utf-8')

    # Generate PDF
    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf)
    pdf.seek(0)

    if pisa_status.err:
        return HttpResponse('There was an error generating the PDF')

    # Return the generated PDF as a response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="resignation_letter_{employee.name}.pdf"'
    return response
