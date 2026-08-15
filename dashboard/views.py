from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from students.models import Student, FormSettings
from students.forms import StudentForm, FormSettingsForm
import datetime
from django.db.models.functions import TruncDate


def admin_login(request):
    """Custom admin login view."""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    return render(request, 'dashboard/login.html')


@login_required(login_url='/admin/login/')
def admin_logout(request):
    """Admin logout view."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('admin_login')


def require_staff(view_func):
    """Decorator to require staff (admin) access."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/admin/login/')
        if not request.user.is_staff:
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('/admin/login/')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


@require_staff
def admin_dashboard(request):
    """Main admin dashboard with statistics."""
    now = timezone.localtime(timezone.now())
    today = now.date()
    week_start = today - datetime.timedelta(days=today.weekday())
    month_start = today.replace(day=1)

    total_students = Student.objects.count()
    today_count = Student.objects.filter(created_at__date=today).count()
    week_count = Student.objects.filter(created_at__date__gte=week_start).count()
    month_count = Student.objects.filter(created_at__date__gte=month_start).count()

    try:
        form_settings = FormSettings.objects.first()
        form_open = form_settings.is_form_open() if form_settings else False
    except Exception:
        form_open = False
        form_settings = None

    recent_students = Student.objects.all()[:10]


    # Chart Data (Last 7 days registrations)
    last_7_days = timezone.now().date() - datetime.timedelta(days=6)
    daily_stats = Student.objects.filter(created_at__date__gte=last_7_days)\
                                 .annotate(date=TruncDate('created_at'))\
                                 .values('date')\
                                 .annotate(count=Count('id'))\
                                 .order_by('date')
    
    date_dict = {str(last_7_days + datetime.timedelta(days=i)): 0 for i in range(7)}
    for stat in daily_stats:
        date_dict[str(stat['date'])] = stat['count']
        
    chart_dates = list(date_dict.keys())
    chart_counts = list(date_dict.values())

    # Pie Chart Data (Program distribution)
    prog_stats = Student.objects.values('program_of_study').annotate(count=Count('id')).order_by('-count')
    pie_labels = [p['program_of_study'] for p in prog_stats]
    pie_data = [p['count'] for p in prog_stats]

    context = {
        'total_students': total_students,
        'today_count': today_count,
        'week_count': week_count,
        'month_count': month_count,
        'form_open': form_open,
        'form_settings': form_settings,
        'recent_students': recent_students,
        'active_page': 'dashboard',
        'chart_dates': chart_dates,
        'chart_counts': chart_counts,
        'pie_labels': pie_labels,
        'pie_data': pie_data,
    }

    return render(request, 'dashboard/dashboard.html', context)


@require_staff
def admin_students(request):
    """Student list with search, filter, and pagination."""
    students = Student.objects.all()
    search_query = request.GET.get('search', '').strip()
    if search_query:
        students = students.filter(
            Q(name__icontains=search_query) |
            Q(enrollment_number__icontains=search_query) |
            Q(exam_registration_number__icontains=search_query) |
            Q(umis_number__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(mobile__icontains=search_query)
        )

    # Filter parameters
    program = request.GET.get('program', '')
    branch = request.GET.get('branch', '')
    year = request.GET.get('year', '')
    gender = request.GET.get('gender', '')
    category = request.GET.get('category', '')
    blood_group = request.GET.get('blood_group', '')
    backlog = request.GET.get('backlog', '')
    career = request.GET.get('career', '')
    relocate = request.GET.get('relocate', '')
    internship = request.GET.get('internship', '')

    if program:
        students = students.filter(program_of_study=program)
    if branch:
        students = students.filter(branch=branch)
    if year:
        students = students.filter(year_of_completion=year)
    if gender:
        students = students.filter(gender=gender)
    if category:
        students = students.filter(category=category)
    if blood_group:
        students = students.filter(blood_group=blood_group)
    if backlog:
        students = students.filter(current_backlog=(backlog == 'yes'))
    if career:
        students = students.filter(career_preference=career)
    if relocate:
        students = students.filter(willingness_to_relocate=relocate)
    if internship:
        if internship == 'yes':
            students = students.exclude(internship_company='')
        else:
            students = students.filter(internship_company='')

    paginator = Paginator(students, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'students': page_obj,
        'search_query': search_query,
        'program': program, 'branch': branch, 'year': year,
        'gender': gender, 'category': category, 'blood_group': blood_group,
        'backlog': backlog, 'career': career, 'relocate': relocate,
        'internship': internship,
        'program_choices': Student.PROGRAM_CHOICES,
        'branch_choices': Student.BRANCH_CHOICES,
        'gender_choices': Student.GENDER_CHOICES,
        'category_choices': Student.CATEGORY_CHOICES,
        'blood_group_choices': Student.BLOOD_GROUP_CHOICES,
        'career_choices': Student.CAREER_CHOICES,
        'relocate_choices': Student.RELOCATE_CHOICES,
        'total_count': students.count(),
        'active_page': 'students',
    }
    return render(request, 'dashboard/students.html', context)


@require_staff
def admin_student_detail(request, pk):
    """View detailed student information."""
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'dashboard/student_detail.html', {'student': student, 'active_page': 'students'})


@require_staff
def admin_student_edit(request, pk):
    """Edit student record."""
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student information updated successfully.')
            return redirect('admin_student_detail', pk=pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-fill the extra fields
        initial = {}
        if student.programming_languages:
            langs = [l.strip() for l in student.programming_languages.split(',')]
            prog_choices = [c[0] for c in StudentForm.PROG_LANG_CHOICES]
            initial['programming_languages_list'] = [l for l in langs if l in prog_choices]
            other_prog = [l for l in langs if l not in prog_choices]
            initial['programming_languages_other'] = ', '.join(other_prog)
        if student.communication_languages:
            langs = [l.strip() for l in student.communication_languages.split(',')]
            comm_choices = [c[0] for c in StudentForm.COMM_LANG_CHOICES]
            initial['communication_languages_list'] = [l for l in langs if l in comm_choices]
            other_comm = [l for l in langs if l not in comm_choices]
            initial['communication_languages_other'] = ', '.join(other_comm)
        if student.nptel_courses:
            courses = student.nptel_courses.split(' | ')
            initial['nptel_course_1'] = courses[0] if len(courses) > 0 else ''
            initial['nptel_course_2'] = courses[1] if len(courses) > 1 else ''
        form = StudentForm(instance=student, initial=initial)

    return render(request, 'dashboard/student_edit.html', {
        'form': form, 'student': student, 'active_page': 'students'
    })


@require_staff
def admin_student_delete(request, pk):
    """Delete student record."""
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        name = student.name
        student.delete()
        messages.success(request, f'Student "{name}" has been deleted successfully.')
        return redirect('admin_students')
    return render(request, 'dashboard/student_delete_confirm.html', {'student': student, 'active_page': 'students'})


@require_staff
def admin_form_control(request):
    """Form opening/closing control."""
    form_settings, created = FormSettings.objects.get_or_create(pk=1)
    if request.method == 'POST':
        form = FormSettingsForm(request.POST, instance=form_settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form settings saved successfully.')
            return redirect('admin_form_control')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FormSettingsForm(instance=form_settings)
    return render(request, 'dashboard/form_control.html', {
        'form': form, 'form_settings': form_settings,
        'form_open': form_settings.is_form_open(),
        'active_page': 'form_control'
    })


@require_staff
def admin_reports(request):
    """Reports page with various analytics."""
    total_students = Student.objects.count()

    program_stats = list(Student.objects.values('program_of_study').annotate(count=Count('id')).order_by('-count'))
    for item in program_stats: item['percent'] = (item['count'] / total_students * 100) if total_students else 0
    branch_stats = list(Student.objects.values('branch').annotate(count=Count('id')).order_by('-count'))
    for item in branch_stats: item['percent'] = (item['count'] / total_students * 100) if total_students else 0
    year_stats = list(Student.objects.values('year_of_completion').annotate(count=Count('id')).order_by('year_of_completion'))
    for item in year_stats: item['percent'] = (item['count'] / total_students * 100) if total_students else 0
    gender_stats = list(Student.objects.values('gender').annotate(count=Count('id')))
    for item in gender_stats: item['percent'] = (item['count'] / total_students * 100) if total_students else 0
    category_stats = list(Student.objects.values('category').annotate(count=Count('id')).order_by('-count'))
    for item in category_stats: item['percent'] = (item['count'] / total_students * 100) if total_students else 0
    career_stats = list(Student.objects.values('career_preference').annotate(count=Count('id')).order_by('-count'))
    for item in career_stats: item['percent'] = (item['count'] / total_students * 100) if total_students else 0
    backlog_yes = Student.objects.filter(current_backlog=True).count()
    backlog_no = total_students - backlog_yes
    internship_yes = Student.objects.exclude(internship_company='').count()
    internship_no = total_students - internship_yes
    backlog_yes_pct = (backlog_yes / total_students * 100) if total_students else 0
    backlog_no_pct = (backlog_no / total_students * 100) if total_students else 0
    internship_yes_pct = (internship_yes / total_students * 100) if total_students else 0
    internship_no_pct = (internship_no / total_students * 100) if total_students else 0

    now = timezone.localtime(timezone.now())
    today = now.date()
    week_start = today - datetime.timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    today_count = Student.objects.filter(created_at__date=today).count()
    week_count = Student.objects.filter(created_at__date__gte=week_start).count()
    month_count = Student.objects.filter(created_at__date__gte=month_start).count()


    return render(request, 'dashboard/reports.html', {
        'total_students': total_students,
        'today_count': today_count,
        'week_count': week_count,
        'month_count': month_count,
        'program_stats': program_stats,
        'branch_stats': branch_stats,
        'year_stats': year_stats,
        'gender_stats': gender_stats,
        'category_stats': category_stats,
        'career_stats': career_stats,
        'backlog_yes': backlog_yes,
        'backlog_no': backlog_no,
        'internship_yes': internship_yes,
        'internship_no': internship_no,
        'backlog_yes_pct': backlog_yes_pct,
        'backlog_no_pct': backlog_no_pct,
        'internship_yes_pct': internship_yes_pct,
        'internship_no_pct': internship_no_pct,
        'active_page': 'reports'
    })


@require_staff
def export_pdf(request):
    """PDF export view."""
    from utils.pdf_generator import generate_students_pdf, generate_student_pdf
    student_id = request.GET.get('student_id')
    if student_id:
        student = get_object_or_404(Student, pk=student_id)
        pdf_buffer = generate_student_pdf(student)
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="student_{student.enrollment_number}.pdf"'
        return response

    # Build filtered queryset same as students list
    students = Student.objects.all()
    search_query = request.GET.get('search', '').strip()
    if search_query:
        students = students.filter(
            Q(name__icontains=search_query) | Q(enrollment_number__icontains=search_query) |
            Q(branch__icontains=search_query) | Q(program_of_study__icontains=search_query)
        )
    program = request.GET.get('program', '')
    branch = request.GET.get('branch', '')
    if program:
        students = students.filter(program_of_study=program)
    if branch:
        students = students.filter(branch=branch)

    pdf_buffer = generate_students_pdf(students)
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="students_report.pdf"'
    return response


@require_staff
def export_excel(request):
    """Excel export view."""
    from utils.excel_generator import generate_students_excel
    students = Student.objects.all()
    search_query = request.GET.get('search', '').strip()
    if search_query:
        students = students.filter(
            Q(name__icontains=search_query) | Q(enrollment_number__icontains=search_query) |
            Q(branch__icontains=search_query) | Q(program_of_study__icontains=search_query)
        )
    program = request.GET.get('program', '')
    branch = request.GET.get('branch', '')
    if program:
        students = students.filter(program_of_study=program)
    if branch:
        students = students.filter(branch=branch)

    excel_buffer = generate_students_excel(students)
    response = HttpResponse(excel_buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="students_data.xlsx"'
    return response
