import re

with open('utils/pdf_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

import_str = """def generate_students_pdf(students):
    \"\"\"Generate PDF for multiple students in an Excel-like tabular format.\"\"\"
    buffer = BytesIO()
    # Create a massive custom page size to fit all 48 columns (160cm x 40cm)
    custom_page_size = (160*cm, 40*cm)
    doc = SimpleDocTemplate(buffer, pagesize=custom_page_size,
                             leftMargin=1.5*cm, rightMargin=1.5*cm,
                             topMargin=1.5*cm, bottomMargin=1.5*cm)
    styles = get_styles()
    story = []

    # Cover page / Header
    story.append(Paragraph("ANNAMALAI UNIVERSITY", styles['title']))
    story.append(Paragraph("Training and Placement Cell (TPC) | Student Data Report", styles['subtitle']))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width='100%', thickness=2, color=PRIMARY_COLOR))
    story.append(Spacer(1, 10))

    now = timezone.localtime(timezone.now())
    student_list = list(students)
    story.append(Paragraph(f"Total Records: {len(student_list)} | Generated: {now.strftime('%d-%m-%Y %H:%M:%S')}", styles['footer']))
    story.append(Spacer(1, 20))

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
"""

# Replace generate_students_pdf function entirely
new_content = re.sub(r'def generate_students_pdf\(students\):.*', import_str.strip(), content, flags=re.DOTALL)

with open('utils/pdf_generator.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Updated PDF generator!')
