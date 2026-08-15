from django.shortcuts import render, redirect
from .models import Student, FormSettings


def index(request):
    """Main landing page."""
    try:
        form_settings = FormSettings.objects.first()
        form_open = form_settings.is_form_open() if form_settings else False
    except Exception:
        form_open = False
    return render(request, 'index.html', {'form_open': form_open})


def student_form(request):
    """Student data collection form."""
    from .forms import StudentForm
    # Check if form is open
    try:
        form_settings = FormSettings.objects.first()
        if not form_settings or not form_settings.is_form_open():
            return redirect('form_closed')
    except Exception:
        return redirect('form_closed')

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_success')
        else:
            return render(request, 'students/student_form.html', {'form': form, 'errors': form.errors})
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form})


def student_success(request):
    """Success page after form submission."""
    return render(request, 'students/success.html')


def form_closed(request):
    """Form closed page."""
    try:
        form_settings = FormSettings.objects.first()
    except Exception:
        form_settings = None
    return render(request, 'students/closed.html', {'form_settings': form_settings})
