"""
PDF Generator using ReportLab for student data export.
"""
from io import BytesIO
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                  TableStyle, HRFlowable, PageBreak)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from django.utils import timezone
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os
from django.conf import settings

# Register custom fonts
try:
    fonts_dir = os.path.join(settings.BASE_DIR, 'static', 'fonts')
    pdfmetrics.registerFont(TTFont('Poppins', os.path.join(fonts_dir, 'Poppins-Regular.ttf')))
    pdfmetrics.registerFont(TTFont('Poppins-Bold', os.path.join(fonts_dir, 'Poppins-Bold.ttf')))
except Exception as e:
    print("Warning: Could not register Poppins font.", e)


# Color palette
PRIMARY_COLOR = colors.HexColor('#1e3a5f')
ACCENT_COLOR = colors.HexColor('#2563eb')
LIGHT_BLUE = colors.HexColor('#dbeafe')
GRAY = colors.HexColor('#6b7280')
LIGHT_GRAY = colors.HexColor('#f3f4f6')
WHITE = colors.white
BLACK = colors.black


def get_styles():
    styles = getSampleStyleSheet()
    custom = {
        'title': ParagraphStyle('title', parent=styles['Normal'],
                                 fontSize=18, fontName='Poppins-Bold',
                                 textColor=PRIMARY_COLOR, alignment=TA_CENTER, spaceAfter=4),
        'subtitle': ParagraphStyle('subtitle', parent=styles['Normal'],
                                    fontSize=12, fontName='Poppins',
                                    textColor=GRAY, alignment=TA_CENTER, spaceAfter=2),
        'section_header': ParagraphStyle('section_header', parent=styles['Normal'],
                                          fontSize=11, fontName='Poppins-Bold',
                                          textColor=WHITE, spaceAfter=6, spaceBefore=8),
        'field_label': ParagraphStyle('field_label', parent=styles['Normal'],
                                       fontSize=9, fontName='Poppins-Bold',
                                       textColor=GRAY),
        'field_value': ParagraphStyle('field_value', parent=styles['Normal'],
                                       fontSize=9, fontName='Poppins',
                                       textColor=BLACK),
        'footer': ParagraphStyle('footer', parent=styles['Normal'],
                                  fontSize=8, fontName='Poppins',
                                  textColor=GRAY, alignment=TA_CENTER),
        'normal': styles['Normal'],
    }
    return custom


def build_student_data_table(student, styles):
    """Build a 2-column table for student data."""
    def row(label, value):
        return [
            Paragraph(label, styles['field_label']),
            Paragraph(str(value) if value is not None else '—', styles['field_value'])
        ]

    bool_val = lambda v: 'Yes' if v else 'No'

    sections = []

    # Section helper
    def section(title, rows_data):
        header_table = Table([[Paragraph(f'  {title}', styles['section_header'])]], colWidths=[17*cm])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), PRIMARY_COLOR),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ]))
        sections.append(header_table)
        data_table = Table(rows_data, colWidths=[6*cm, 11*cm])
        data_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), LIGHT_GRAY),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [WHITE, LIGHT_GRAY]),
            ('FONTNAME', (0, 0), (0, -1), 'Poppins-Bold'),
            ('FONTNAME', (1, 0), (-1, -1), 'Poppins'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (0, -1), GRAY),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
        ]))
        sections.append(data_table)
        sections.append(Spacer(1, 8))

    # Personal Info
    section('PERSONAL INFORMATION', [
        row('Name', student.name),
        row('Enrollment Number', student.enrollment_number),
        row('Exam Reg. Number', student.exam_registration_number),
        row('UMIS Number', student.umis_number),
        row('Program of Study', student.program_of_study),
        row('Branch/Discipline', student.branch),
        row('Year of Completion', student.year_of_completion),
        row('Email ID', student.email),
        row('Mobile Number', student.mobile),
        row('Alternate Mobile', student.alternate_mobile or '—'),
        row('Date of Birth', student.date_of_birth.strftime('%d-%m-%Y') if student.date_of_birth else '—'),
        row('Gender', student.gender),
        row('Category', student.category),
        row('Blood Group', student.blood_group),
    ])

    # Identification
    section('IDENTIFICATION INFORMATION', [
        row('PAN Number', student.pan_number or '—'),
        row('Aadhaar Number', f"XXXX-XXXX-{student.aadhaar_number[-4:]}" if student.aadhaar_number and len(student.aadhaar_number) >= 4 else '—'),
        row('Passport Number', student.passport_number or '—'),
    ])

    # Family
    section('FAMILY INFORMATION', [
        row('Permanent Address', student.permanent_address),
        row("Guardian's Name", student.guardian_name),
        row("Guardian's Mobile", student.guardian_mobile),
        row("Guardian's Occupation", student.guardian_occupation),
        row('Annual Income (₹)', f"₹{student.guardian_annual_income:,}"),
    ])

    # Academic
    section('ACADEMIC INFORMATION', [
        row('10th Percentage', f"{student.tenth_percentage}%"),
        row('Year of 10th Passing', student.tenth_passing_year),
        row('12th Percentage', f"{student.twelfth_percentage}%" if student.twelfth_percentage else 'N/A'),
        row('Year of 12th Passing', student.twelfth_passing_year or 'N/A'),
        row('Diploma Percentage', f"{student.diploma_percentage}%" if student.diploma_percentage else 'N/A'),
        row('Year of Diploma Passing', student.diploma_passing_year or 'N/A'),
        row('OGPA (Till 5th Sem)', student.ogpa),
    ])

    # Arrears
    section('ARREARS INFORMATION', [
        row('History of Arrears', bool_val(student.history_of_arrears)),
        row('Current Backlog', bool_val(student.current_backlog)),
        row('Number of Backlogs', student.number_of_backlogs if student.current_backlog else 'N/A'),
        row('Remarks / Gap Reason', student.remarks or '—'),
    ])

    # Skills
    section('SKILLS INFORMATION', [
        row('Programming Languages', student.programming_languages or '—'),
        row('Communication Languages', student.communication_languages or '—'),
        row('Additional Skills', student.additional_skills or '—'),
    ])

    # Internship
    section('INTERNSHIP INFORMATION', [
        row('Internship Company', student.internship_company or '—'),
        row('Internship Dates', student.internship_dates or '—'),
    ])

    # Facilities
    section('FACILITIES', [
        row('Laptop/Desktop (Webcam & Mic)', bool_val(student.laptop_desktop)),
        row('High-Speed Internet', bool_val(student.high_speed_internet)),
    ])

    # Career
    section('CAREER PREFERENCE', [
        row('Career Preference', student.career_preference),
        row('Willingness to Relocate', student.willingness_to_relocate),
    ])

    # Courses
    section('COURSES & FUTURE INTERNSHIP', [
        row('NPTEL/SWAYAM Courses', student.nptel_courses or '—'),
        row('Future Internship (Dec 26 - Apr 27)', bool_val(student.future_internship)),
    ])

    # Declaration
    section('DECLARATION', [
        row('TPC Rules Acceptance', 'Accepted' if student.tpc_acceptance else 'Not Accepted'),
        row('Submitted On', student.created_at.strftime('%d-%m-%Y %H:%M') if student.created_at else '—'),
    ])

    return sections


def generate_student_pdf(student):
    """Generate PDF for a single student."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                             leftMargin=2*cm, rightMargin=2*cm,
                             topMargin=2*cm, bottomMargin=2*cm)
    styles = get_styles()
    story = []

    # Header
    story.append(Paragraph("ANNAMALAI UNIVERSITY", styles['title']))
    story.append(Paragraph("Training and Placement Cell (TPC)", styles['subtitle']))
    story.append(Paragraph("Student Data Collection Form", styles['subtitle']))
    story.append(HRFlowable(width='100%', thickness=2, color=PRIMARY_COLOR))
    story.append(Spacer(1, 12))

    # Student sections
    story.extend(build_student_data_table(student, styles))

    # Footer
    now = timezone.localtime(timezone.now())
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width='100%', thickness=1, color=GRAY))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        f"Generated on: {now.strftime('%d-%m-%Y')} at {now.strftime('%H:%M:%S')} | "
        f"Training and Placement Cell",
        styles['footer']
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_students_pdf(students):
    """Generate PDF for multiple students in an Excel-like tabular format."""
    buffer = BytesIO()
    # Create a massive custom page size to fit all 48 columns (160cm x 40cm)
    custom_page_size = (160*cm, 40*cm)
    doc = SimpleDocTemplate(buffer, pagesize=custom_page_size,
                             leftMargin=1.5*cm, rightMargin=1.5*cm,
                             topMargin=1.5*cm, bottomMargin=1.5*cm)
    styles = get_styles()
    story = []

    # Cover page / Header
    title_style = ParagraphStyle('massive_title', parent=styles['title'], fontSize=26, spaceAfter=14, leading=30)
    subtitle_style = ParagraphStyle('massive_sub', parent=styles['subtitle'], fontSize=16, spaceAfter=14, leading=20)
    
    story.append(Paragraph("ANNAMALAI UNIVERSITY", title_style))
    story.append(Paragraph("Training and Placement Cell (TPC) | Student Data Report", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width='100%', thickness=2, color=PRIMARY_COLOR))
    story.append(Spacer(1, 10))

    story.append(Spacer(1, 15))

    now = timezone.localtime(timezone.now())
    student_list = list(students)
    footer_style = ParagraphStyle('massive_footer', parent=styles['footer'], fontSize=12)
    story.append(Paragraph(f"Total Records: {len(student_list)} | Generated: {now.strftime('%d-%m-%Y %H:%M:%S')}", footer_style))
    story.append(Spacer(1, 25))

    # === Column Headers (same as Excel) ===
    headers = [
        'S.No.', 'Student Name', 'Enrollment No.', 'Exam Reg. No.',
        'UMIS No.', 'Program', 'Branch/Discipline', 'Year',
        'Email ID', 'Mobile Number', 'Alt. Mobile', 'Date of Birth',
        'Gender', 'Category', 'Blood',
        'PAN Number', 'Aadhaar No.', 'Passport No.',
        'Permanent Address', "Guardian's Name", "Guardian's Mobile",
        "Guardian's Occ.", 'Income (Rs)',
        '10th %', '10th Year',
        '12th %', '12th Year',
        'Dip. %', 'Dip. Year',
        'OGPA',
        'Arr. Hist.', 'Cur. Backlog', 'Backlogs',
        'Remarks/Gap',
        'Prog. Langs', 'Comm. Langs', 'Add. Skills',
        'Internship Co.', 'Internship Dates',
        'Laptop/PC', 'Internet',
        'Career Pref.', 'Relocate',
        'NPTEL', 'Fut. Intern',
        'TPC Accept', 'Sub. Date', 'Sub. Time'
    ]
    table_data = [headers]

    bool_val = lambda v: 'Yes' if v else 'No'

    for idx, s in enumerate(student_list, 1):
        aadhaar_masked = f"XXXX-XXXX-{s.aadhaar_number[-4:]}" if s.aadhaar_number and len(s.aadhaar_number) >= 4 else '—'
        table_data.append([
            str(idx), s.name, s.enrollment_number, s.exam_registration_number,
            s.umis_number, s.program_of_study, s.branch, str(s.year_of_completion),
            s.email, s.mobile, s.alternate_mobile or '—',
            s.date_of_birth.strftime('%d-%m-%Y') if s.date_of_birth else '—',
            s.gender, s.category, s.blood_group,
            s.pan_number or '—', aadhaar_masked, s.passport_number or '—',
            s.permanent_address, s.guardian_name, s.guardian_mobile,
            s.guardian_occupation, f"Rs.{s.guardian_annual_income}",
            f"{s.tenth_percentage}%", str(s.tenth_passing_year),
            f"{s.twelfth_percentage}%" if s.twelfth_percentage else '—', str(s.twelfth_passing_year or '—'),
            f"{s.diploma_percentage}%" if s.diploma_percentage else '—', str(s.diploma_passing_year or '—'),
            str(s.ogpa),
            bool_val(s.history_of_arrears), bool_val(s.current_backlog), str(s.number_of_backlogs),
            s.remarks or '—',
            s.programming_languages or '—', s.communication_languages or '—', s.additional_skills or '—',
            s.internship_company or '—', s.internship_dates or '—',
            bool_val(s.laptop_desktop), bool_val(s.high_speed_internet),
            s.career_preference, s.willingness_to_relocate,
            s.nptel_courses or '—', bool_val(s.future_internship),
            'Accepted' if s.tpc_acceptance else 'Not Accepted',
            s.created_at.strftime('%d-%m-%Y') if s.created_at else '—',
            s.created_at.strftime('%H:%M:%S') if s.created_at else '—'
        ])

    # Convert Excel col widths to roughly cm widths
    col_widths_cm = [
        1.5, 5, 4, 4, 3.5, 3.5, 6, 2, 6, 3, 3, 2.5,
        2, 2.5, 2, 2.5, 3, 3, 8, 5, 3, 4, 3,
        2, 2, 2, 2, 2.5, 2, 1.5,
        2, 2, 2, 6,
        6, 6, 6, 5, 4,
        3.5, 3, 4, 3.5,
        6, 2.5, 2.5, 2.5, 2.5
    ]
    col_widths = [w * cm for w in col_widths_cm]

    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Poppins-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Poppins'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t)

    doc.build(story)
    buffer.seek(0)
    return buffer