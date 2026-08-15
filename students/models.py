from django.db import models
from django.utils import timezone


class Student(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    CATEGORY_CHOICES = [
        ('OC', 'OC (Open Category)'),
        ('BC', 'BC (Backward Class)'),
        ('BC(M)', 'BC(M) (Backward Class Muslim)'),
        ('MBC', 'MBC (Most Backward Class)'),
        ('SC', 'SC (Scheduled Caste)'),
        ('SCA', 'SCA (Scheduled Caste Arunthathiyar)'),
        ('ST', 'ST (Scheduled Tribe)'),
    ]
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    CAREER_CHOICES = [
        ('Campus Placement', 'Campus Placement'),
        ('Higher Studies', 'Higher Studies'),
        ('Entrepreneurship', 'Entrepreneurship'),
        ('Campus Placement & Higher Studies', 'Campus Placement & Higher Studies'),
        ('All', 'All'),
    ]
    RELOCATE_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Depends on Location', 'Depends on Location'),
    ]
    PROGRAM_CHOICES = [
        ('B.E.', 'B.E. (Bachelor of Engineering)'),
        ('B.Tech.', 'B.Tech. (Bachelor of Technology)'),
        ('M.E.', 'M.E. (Master of Engineering)'),
        ('M.Tech.', 'M.Tech. (Master of Technology)'),
        ('MBA', 'MBA'),
        ('MCA', 'MCA'),
        ('Other', 'Other'),
    ]
    BRANCH_CHOICES = [
        ('Civil Engineering', 'Civil Engineering'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Electrical & Electronics Engineering', 'Electrical & Electronics Engineering'),
        ('Electronics & Communication Engineering', 'Electronics & Communication Engineering'),
        ('Computer Science & Engineering', 'Computer Science & Engineering'),
        ('Information Technology', 'Information Technology'),
        ('Chemical Engineering', 'Chemical Engineering'),
        ('Aeronautical Engineering', 'Aeronautical Engineering'),
        ('Automobile Engineering', 'Automobile Engineering'),
        ('Biomedical Engineering', 'Biomedical Engineering'),
        ('Biotechnology', 'Biotechnology'),
        ('Agriculture Engineering', 'Agriculture Engineering'),
        ('Artificial Intelligence & Data Science', 'Artificial Intelligence & Data Science'),
        ('Artificial Intelligence & Machine Learning', 'Artificial Intelligence & Machine Learning'),
        ('Cyber Security', 'Cyber Security'),
        ('Other', 'Other'),
    ]

    # Personal Information
    name = models.CharField(max_length=200, verbose_name="Name of the Student")
    enrollment_number = models.CharField(max_length=50, unique=True, verbose_name="Enrollment Number")
    exam_registration_number = models.CharField(max_length=50, unique=True, verbose_name="Exam Registration Number")
    umis_number = models.CharField(max_length=50, unique=True, verbose_name="UMIS Number")
    program_of_study = models.CharField(max_length=100, choices=PROGRAM_CHOICES, verbose_name="Program of Study")
    branch = models.CharField(max_length=100, choices=BRANCH_CHOICES, verbose_name="Discipline/Branch")
    year_of_completion = models.IntegerField(verbose_name="Year of Completion")
    email = models.EmailField(verbose_name="Email ID")
    mobile = models.CharField(max_length=15, verbose_name="Mobile Number")
    alternate_mobile = models.CharField(max_length=15, blank=True, verbose_name="Alternate Mobile Number")
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Gender")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Category (Community)")
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, verbose_name="Blood Group")

    # Identification Information
    pan_number = models.CharField(max_length=10, blank=True, verbose_name="PAN Number")
    aadhaar_number = models.CharField(max_length=12, blank=True, verbose_name="Aadhaar Number")
    passport_number = models.CharField(max_length=20, blank=True, verbose_name="Passport Number")

    # Family Information
    permanent_address = models.TextField(verbose_name="Permanent Address")
    guardian_name = models.CharField(max_length=200, verbose_name="Father's/Guardian's Name")
    guardian_mobile = models.CharField(max_length=15, verbose_name="Father's/Guardian's Mobile Number")
    guardian_occupation = models.CharField(max_length=200, verbose_name="Father's/Guardian's Occupation")
    guardian_annual_income = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Father's/Guardian's Annual Income")

    # Academic Information
    tenth_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="10th Pass Percentage")
    tenth_passing_year = models.IntegerField(verbose_name="Year of 10th Passing")
    twelfth_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="12th Pass Percentage")
    twelfth_passing_year = models.IntegerField(blank=True, null=True, verbose_name="Year of 12th Passing")
    diploma_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Diploma Pass Percentage")
    diploma_passing_year = models.IntegerField(blank=True, null=True, verbose_name="Year of Passing Diploma")
    ogpa = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="OGPA (Till 5th Semester)")

    # Arrears Information
    history_of_arrears = models.BooleanField(default=False, verbose_name="History of Arrears")
    current_backlog = models.BooleanField(default=False, verbose_name="Current Backlog (Standing Arrears)")
    number_of_backlogs = models.IntegerField(default=0, verbose_name="Number of Backlogs")
    remarks = models.TextField(blank=True, verbose_name="Remarks / Year Gap Reason")

    # Skills Information
    programming_languages = models.TextField(blank=True, verbose_name="Programming Languages Known")
    communication_languages = models.TextField(blank=True, verbose_name="Communication (Spoken) Languages Known")
    additional_skills = models.TextField(blank=True, verbose_name="Additional Skill Set")

    # Internship Information
    internship_company = models.CharField(max_length=300, blank=True, verbose_name="Internship Company")
    internship_dates = models.CharField(max_length=200, blank=True, verbose_name="Internship Dates")

    # Facilities
    laptop_desktop = models.BooleanField(default=False, verbose_name="Laptop/Desktop with Webcam & Mic")
    high_speed_internet = models.BooleanField(default=False, verbose_name="High-Speed Internet Connection")

    # Career Preference
    career_preference = models.CharField(max_length=100, choices=CAREER_CHOICES, verbose_name="Career Preference")
    willingness_to_relocate = models.CharField(max_length=30, choices=RELOCATE_CHOICES, verbose_name="Willingness to Relocate")

    # Courses
    nptel_courses = models.TextField(blank=True, verbose_name="NPTEL/SWAYAM Courses Completed")
    future_internship = models.BooleanField(default=False, verbose_name="Willing for Internship (Dec 2026 - Apr 2027)")

    # Declaration
    tpc_acceptance = models.BooleanField(default=False, verbose_name="TPC Rules Acceptance")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.name} ({self.enrollment_number})"


class FormSettings(models.Model):
    is_active = models.BooleanField(default=True, verbose_name="Form Status")
    opening_date = models.DateField(blank=True, null=True, verbose_name="Opening Date")
    opening_time = models.TimeField(blank=True, null=True, verbose_name="Opening Time")
    closing_date = models.DateField(blank=True, null=True, verbose_name="Closing Date")
    closing_time = models.TimeField(blank=True, null=True, verbose_name="Closing Time")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Form Settings'
        verbose_name_plural = 'Form Settings'

    def __str__(self):
        return f"Form Settings - {'OPEN' if self.is_active else 'CLOSED'}"

    def is_form_open(self):
        """Check if form is currently open based on date/time settings."""
        from django.utils import timezone
        import datetime
        if not self.is_active:
            return False
        now = timezone.localtime(timezone.now())
        now_date = now.date()
        now_time = now.time()
        if self.opening_date and self.opening_time:
            opening_dt = datetime.datetime.combine(self.opening_date, self.opening_time)
            if now_date < self.opening_date or (now_date == self.opening_date and now_time < self.opening_time):
                return False
        if self.closing_date and self.closing_time:
            if now_date > self.closing_date or (now_date == self.closing_date and now_time > self.closing_time):
                return False
        return True
