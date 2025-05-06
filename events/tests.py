from django.test import TestCase
from django.utils import timezone

from accounts.models import CustomUser
from courses.models import Course
from events.models import Events
from django.contrib.auth.models import Group

# Diese Methode wurde mithilfe von ChatGPT (OpenAI) in Hinblick auf bestimmte Aspekte verbessert und manuell angepasst
class EventsTestcase(TestCase):
    def setUp(self):
        Group.objects.get_or_create(id=1, name='Student')
        Group.objects.get_or_create(id=2, name='Teacher')
        user1 = CustomUser.objects.create_user(username='test1', email='test@gmail.com', password='iamatest1234')
        user2 = CustomUser.objects.create_user(username='test2', email='test2@gmail.com', password='iamatest1234')
        user1.groups.add(1)
        user2.groups.add(2)
        user1.save()
        user2.save()
        course = Course.objects.create(title='Testkurs',description='Test', start_date=timezone.now(), end_date=timezone.now())
        course.students.add(user1.id)
        course.teachers.add(user2.id)
        course.save()
        events = Events.objects.create(description='Testbeschreibung',start_date=timezone.now(), end_date=timezone.now(),course=course)
        events.save()
    def test_event_binding(self):
        x = Events.objects.filter(course__title='Testkurs')[0]
        self.assertEqual(x.description, 'Testbeschreibung')
        temp = False
        for f in x.course.teachers.all():
            if f.email == 'test2@gmail.com':
                temp = True
        self.assertTrue(
            temp
        )