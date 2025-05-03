import json
import os
from django.conf import settings
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from weasyprint import HTML
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from grades.models import Grade
from courses.models import Course


@csrf_exempt
def create_certificate(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_ids = data.get('user_ids', [])

            course = Course.objects.prefetch_related('teachers').get(id=id)
            teacher_text = 'Lehrkräfte: <br>'
            for teacher in course.teachers.all():
                teacher_text += f'{teacher.first_name} {teacher.last_name}<br>'

            for user_id in user_ids:
                grade_text = 'Noten:'
                grade_nr = 1
                endgrade = 0
                user = User.objects.get(id=user_id)
                grades = Grade.objects.filter(
                    submission__user=user,
                    submission__assignment__course_id=course.id
                )

                for grade in grades:
                    endgrade += int(grade.grade)
                    grade_text += f'<p>Note {grade_nr}: {grade.grade}</p><br>'
                    grade_nr += 1

                endgrade = round(endgrade / len(grades), 2) if grades else 0
                grade_text += f'<hr><p>Endnote: {endgrade}</p>'

                pdf_path = create_pdf(user.first_name, user.last_name, grade_text, teacher_text, course.name)
                send_email(user.email, pdf_path)

            return JsonResponse({'status': 'success'})

        except Course.DoesNotExist:
            return JsonResponse({'error': 'Course not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def create_pdf(firstname, lastname, gradetext, teachertext, course_name):
    html_content = render_to_string("certificate_template.html", {
        'firstname': firstname,
        'lastname': lastname,
        'grades_html': gradetext,
        'teachers_html': teachertext,
        'course': course_name,
    })

    filename = f"Zertifikat_{course_name}_{lastname}_{firstname}.pdf"
    output_path = os.path.join(settings.MEDIA_ROOT, 'certificates', filename)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    HTML(string=html_content).write_pdf(output_path)
    return output_path


def send_email(email, pdf_path):
    subject = "Ihr Teilnahmezertifikat"
    message = "Im Anhang finden Sie Ihr Teilnahmezertifikat als PDF-Datei."
    email_msg = EmailMessage(subject, message, to=[email])

    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as f:
            email_msg.attach(os.path.basename(pdf_path), f.read(), 'application/pdf')

    email_msg.send()
