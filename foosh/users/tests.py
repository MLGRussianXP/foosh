from unittest.mock import patch

from cities_light.models import City

from django.contrib.auth import get_user_model
from django.core import management
from django.test import TestCase, override_settings

from django_recaptcha.client import RecaptchaResponse

from users.forms import SchoolSignUpForm, StudentSignUpForm
from users.models import School, Student


__all__ = []


def setUpModule():
    management.call_command(
        "cities_light_fixtures",
        "load",
        base_url="file:fixtures/cities_light/",
    )


class AbstractTests(TestCase):
    def setUp(self):
        self.city = City.objects.get(name="Moscow")


class UserModelTests(AbstractTests):
    def test_create_student(self):
        user = get_user_model()
        student = user.objects.create_user(
            email="student@example.com",
            password="testpassword",
            is_student=True,
        )
        student_student = Student.objects.create(
            user=student,
            name="John",
            surname="Doe",
            patronymic="Smith",
        )
        self.assertTrue(student.is_student)
        self.assertFalse(student.is_school)
        self.assertEqual(student_student.name, "John")
        self.assertEqual(student_student.surname, "Doe")
        self.assertEqual(student_student.patronymic, "Smith")

    def test_create_school(self):
        user = get_user_model()
        school = user.objects.create_user(
            email="school@example.com",
            password="testpassword",
            is_school=True,
        )
        school_school = School.objects.create(
            user=school,
            name="XYZ School",
            city=self.city,
        )
        self.assertTrue(school.is_school)
        self.assertFalse(school.is_student)
        self.assertEqual(school_school.name, "XYZ School")
        self.assertEqual(school_school.city, self.city)


@override_settings(DJANGO_TEST=True)
class FormTests(AbstractTests):
    @patch("django_recaptcha.fields.client.submit")
    def test_student_signup_form_valid(self, mocked_submit):
        mocked_submit.return_value = RecaptchaResponse(is_valid=True)
        user = get_user_model()
        school = user.objects.create_user(
            email="school@example.com",
            password="testpassword",
            is_school=True,
        )
        school_school = School.objects.create(
            user=school,
            name="XYZ School",
            city=self.city,
        )
        form = StudentSignUpForm(
            data={
                "email": "test@example.com",
                "password1": "123123qq",
                "password2": "123123qq",
                "name": "John",
                "surname": "Doe",
                "patronymic": "Smith",
                "city": self.city.id,
                "school": school_school,
                "g-recaptcha-response": "PASSED",
            },
        )
        self.assertTrue(form.is_valid())

    @patch("django_recaptcha.fields.client.submit")
    def test_school_signup_form_valid(self, mocked_submit):
        mocked_submit.return_value = RecaptchaResponse(is_valid=True)
        form = SchoolSignUpForm(
            data={
                "email": "test@example.com",
                "password1": "123123qq",
                "password2": "123123qq",
                "name": "XYZ School",
                "city": self.city,
                "g-recaptcha-response": "PASSED",
            },
        )
        self.assertTrue(form.is_valid())
