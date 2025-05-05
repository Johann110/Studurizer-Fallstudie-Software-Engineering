import json
import os
from django.conf import settings
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from reportlab.lib.colors import hue2rgb
import logging
from StudurizerApp.utils import send_email_notification, logger
from accounts.models import CustomUser, UserProfile
from grades.models import Grade
from courses.models import Course
from xhtml2pdf import pisa
from django.template.loader import render_to_string
import os
from django.conf import settings

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
                teacher_img_url = UserProfile.objects.filter(user_id=teacher.id).get().signature.url
                teacher_img_path = os.path.join(settings.MEDIA_ROOT, teacher_img_url.replace(settings.MEDIA_URL, ''))
                teacher_img_path = teacher_img_path.replace('/', os.sep).replace('\\', os.sep)
                logging.debug(f"Teacher image path: {teacher_img_path}")
                if os.path.exists(teacher_img_path):
                    teacher_text += f'<img src="{teacher_img_path}" width="200px" height="50px"/> <br>'
            for user_id in user_ids:
                grade_text = 'Noten:'
                grade_nr = 1
                endgrade = 0
                user = CustomUser.objects.get(id=user_id)
                grades = Grade.objects.filter(
                    submission__user_id=user_id,
                    submission__assignment__course_id=course.id
                )
                if(grades.count() == 0):
                    print("nix")
                else:
                    for grade in grades:
                        endgrade += int(grade.grade)
                        grade_text += f'<p>Note {grade_nr}: {grade.grade}</p>'
                        grade_nr += 1
                        logger.debug(f"Current endgrade: {endgrade}")
                    endgrade = round(endgrade / len(grades), 2) if grades else 0
                    grade_text += f'<p>Endnote: {endgrade}</p>'
                    pdf_path = create_pdf(user.first_name, user.last_name, grade_text, teacher_text, course.title)
                    send_email_notification(
                        to_email=user.email,
                        subject="Ihr Teilnahmezertifikat",
                        body="Im Anhang finden Sie Ihr Teilnahmezertifikat als PDF-Datei.",
                        attachment_path=pdf_path
                    )

            return JsonResponse({'status': 'success'})

        except Course.DoesNotExist:
            print('Course does not exist')
            return JsonResponse({'error': 'Course not found'}, status=404)
        except Exception as e:
            logging.error('An unexpected error occurred while creating the certificate.', exc_info=True)
            return JsonResponse({'error': str(e)}, status=500)
    else:
        print('wrong method')
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
    with open(output_path, "wb") as result_file:
        pisa.CreatePDF(html_content, dest=result_file)

    return output_path

