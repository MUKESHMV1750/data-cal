from django import forms
from .models import Student, FormSettings
import re


class StudentForm(forms.ModelForm):
    # NPTEL courses as two separate fields
    nptel_course_1 = forms.CharField(max_length=200, required=False, label="NPTEL/SWAYAM Course 1",
                                      widget=forms.TextInput(attrs={'placeholder': 'Course 1 name & completion year'}))
    nptel_course_2 = forms.CharField(max_length=200, required=False, label="NPTEL/SWAYAM Course 2",
                                      widget=forms.TextInput(attrs={'placeholder': 'Course 2 name & completion year'}))

    PROG_LANG_CHOICES = [
        ('Python', 'Python'), ('Java', 'Java'), ('C', 'C'), ('C++', 'C++'),
        ('JavaScript', 'JavaScript'), ('SQL', 'SQL'), ('R', 'R'),
        ('MATLAB', 'MATLAB'), ('PHP', 'PHP'), ('Swift', 'Swift'),
    ]
    COMM_LANG_CHOICES = [
        ('Tamil', 'Tamil'), ('English', 'English'), ('Hindi', 'Hindi'),
        ('Telugu', 'Telugu'), ('Kannada', 'Kannada'), ('Malayalam', 'Malayalam'),
        ('French', 'French'), ('German', 'German'),
    ]

    programming_languages_list = forms.MultipleChoiceField(
        choices=PROG_LANG_CHOICES, required=False, widget=forms.CheckboxSelectMultiple(),
        label="Programming Languages Known"
    )
    programming_languages_other = forms.CharField(max_length=300, required=False,
                                                   widget=forms.TextInput(attrs={'placeholder': 'Other languages...'}),
                                                   label="Other Programming Languages")
    communication_languages_list = forms.MultipleChoiceField(
        choices=COMM_LANG_CHOICES, required=False, widget=forms.CheckboxSelectMultiple(),
        label="Communication Languages Known"
    )
    communication_languages_other = forms.CharField(max_length=300, required=False,
                                                     widget=forms.TextInput(attrs={'placeholder': 'Other languages...'}),
                                                     label="Other Communication Languages")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        skip = {'programming_languages_list', 'communication_languages_list',
                'tpc_acceptance', 'history_of_arrears', 'current_backlog',
                'laptop_desktop', 'high_speed_internet', 'future_internship'}
        for name, field in self.fields.items():
            if name in skip:
                continue
            widget = field.widget
            existing = widget.attrs.get('class', '')
            if 'form-control' not in existing:
                widget.attrs['class'] = ('form-control ' + existing).strip()

    class Meta:
        model = Student
        exclude = ['programming_languages', 'communication_languages', 'nptel_courses', 'created_at', 'updated_at']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'enrollment_number': forms.TextInput(attrs={'placeholder': 'Enrollment Number'}),
            'exam_registration_number': forms.TextInput(attrs={'placeholder': 'Exam Registration Number'}),
            'umis_number': forms.TextInput(attrs={'placeholder': 'UMIS Number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@example.com'}),
            'mobile': forms.TextInput(attrs={'placeholder': '10-digit mobile number', 'maxlength': '10'}),
            'alternate_mobile': forms.TextInput(attrs={'placeholder': '10-digit alternate number', 'maxlength': '10'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'pan_number': forms.TextInput(attrs={'placeholder': 'ABCDE1234F', 'maxlength': '10', 'style': 'text-transform:uppercase'}),
            'aadhaar_number': forms.TextInput(attrs={'placeholder': '12-digit Aadhaar', 'maxlength': '12'}),
            'passport_number': forms.TextInput(attrs={'placeholder': 'Passport Number'}),
            'permanent_address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Full permanent address'}),
            'guardian_name': forms.TextInput(attrs={'placeholder': "Father's/Guardian's Name"}),
            'guardian_mobile': forms.TextInput(attrs={'placeholder': "Father's/Guardian's Mobile", 'maxlength': '10'}),
            'guardian_occupation': forms.TextInput(attrs={'placeholder': 'Occupation'}),
            'guardian_annual_income': forms.NumberInput(attrs={'placeholder': 'Annual income in ₹', 'min': '0'}),
            'tenth_percentage': forms.NumberInput(attrs={'placeholder': '0-100', 'min': '0', 'max': '100', 'step': '0.01'}),
            'tenth_passing_year': forms.NumberInput(attrs={'placeholder': 'YYYY', 'min': '1990', 'max': '2035'}),
            'twelfth_percentage': forms.NumberInput(attrs={'placeholder': '0-100', 'min': '0', 'max': '100', 'step': '0.01'}),
            'twelfth_passing_year': forms.NumberInput(attrs={'placeholder': 'YYYY', 'min': '1990', 'max': '2035'}),
            'diploma_percentage': forms.NumberInput(attrs={'placeholder': '0-100', 'min': '0', 'max': '100', 'step': '0.01'}),
            'diploma_passing_year': forms.NumberInput(attrs={'placeholder': 'YYYY', 'min': '1990', 'max': '2035'}),
            'ogpa': forms.NumberInput(attrs={'placeholder': '0.00-10.00', 'min': '0', 'max': '10', 'step': '0.01'}),
            'number_of_backlogs': forms.NumberInput(attrs={'min': '0'}),
            'remarks': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Remarks or reason for any year gap'}),
            'additional_skills': forms.Textarea(attrs={'rows': 3, 'placeholder': 'e.g. Machine Learning, Web Development...'}),
            'internship_company': forms.TextInput(attrs={'placeholder': 'Company name (if any)'}),
            'internship_dates': forms.TextInput(attrs={'placeholder': 'e.g. Jan 2025 - Mar 2025'}),
        }

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile', '')
        if not re.match(r'^[6-9]\d{9}$', mobile):
            raise forms.ValidationError('Enter a valid 10-digit mobile number starting with 6-9.')
        return mobile

    def clean_alternate_mobile(self):
        alt = self.cleaned_data.get('alternate_mobile', '')
        if alt and not re.match(r'^[6-9]\d{9}$', alt):
            raise forms.ValidationError('Enter a valid 10-digit alternate mobile number.')
        return alt

    def clean_guardian_mobile(self):
        mob = self.cleaned_data.get('guardian_mobile', '')
        if not re.match(r'^[6-9]\d{9}$', mob):
            raise forms.ValidationError("Enter a valid 10-digit Guardian's mobile number.")
        return mob

    def clean_pan_number(self):
        pan = self.cleaned_data.get('pan_number', '').upper()
        if pan and not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', pan):
            raise forms.ValidationError('Enter a valid PAN number (e.g., ABCDE1234F).')
        return pan

    def clean_aadhaar_number(self):
        aadhaar = self.cleaned_data.get('aadhaar_number', '')
        if aadhaar and not re.match(r'^\d{12}$', aadhaar):
            raise forms.ValidationError('Aadhaar number must be exactly 12 digits.')
        return aadhaar

    def clean_tenth_percentage(self):
        val = self.cleaned_data.get('tenth_percentage')
        if val is not None and not (0 <= float(val) <= 100):
            raise forms.ValidationError('Percentage must be between 0 and 100.')
        return val

    def clean_twelfth_percentage(self):
        val = self.cleaned_data.get('twelfth_percentage')
        if val is not None and not (0 <= float(val) <= 100):
            raise forms.ValidationError('Percentage must be between 0 and 100.')
        return val

    def clean_diploma_percentage(self):
        val = self.cleaned_data.get('diploma_percentage')
        if val is not None and not (0 <= float(val) <= 100):
            raise forms.ValidationError('Percentage must be between 0 and 100.')
        return val

    def clean_ogpa(self):
        val = self.cleaned_data.get('ogpa')
        if val is not None and not (0 <= float(val) <= 10):
            raise forms.ValidationError('OGPA must be between 0.00 and 10.00.')
        return val

    def clean_tpc_acceptance(self):
        accepted = self.cleaned_data.get('tpc_acceptance')
        if not accepted:
            raise forms.ValidationError('You must accept the TPC rules and regulations to submit the form.')
        return accepted

    def save(self, commit=True):
        instance = super().save(commit=False)
        prog_langs = list(self.cleaned_data.get('programming_languages_list', []))
        other_prog = self.cleaned_data.get('programming_languages_other', '').strip()
        if other_prog:
            prog_langs.append(other_prog)
        instance.programming_languages = ', '.join(prog_langs)

        comm_langs = list(self.cleaned_data.get('communication_languages_list', []))
        other_comm = self.cleaned_data.get('communication_languages_other', '').strip()
        if other_comm:
            comm_langs.append(other_comm)
        instance.communication_languages = ', '.join(comm_langs)

        c1 = self.cleaned_data.get('nptel_course_1', '').strip()
        c2 = self.cleaned_data.get('nptel_course_2', '').strip()
        courses = [c for c in [c1, c2] if c]
        instance.nptel_courses = ' | '.join(courses)

        if commit:
            instance.save()
        return instance


class FormSettingsForm(forms.ModelForm):
    class Meta:
        model = FormSettings
        fields = ['is_active', 'opening_date', 'opening_time', 'closing_date', 'closing_time']
        widgets = {
            'opening_date': forms.DateInput(attrs={'type': 'date'}),
            'opening_time': forms.TimeInput(attrs={'type': 'time'}),
            'closing_date': forms.DateInput(attrs={'type': 'date'}),
            'closing_time': forms.TimeInput(attrs={'type': 'time'}),
        }
