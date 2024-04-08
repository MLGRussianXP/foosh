from django.contrib.auth import get_user_model
from django.test import TestCase

from users.forms import SchoolSignUpForm, StudentSignUpForm
from users.models import School, Student


__all__ = []


class UserModelTests(TestCase):
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
            city="City Name",
        )
        self.assertTrue(school.is_school)
        self.assertFalse(school.is_student)
        self.assertEqual(school_school.name, "XYZ School")
        self.assertEqual(school_school.city, "City Name")


class FormTests(TestCase):
    def test_student_signup_form_valid(self):
        user = get_user_model()
        school = user.objects.create_user(
            email="school@example.com",
            password="testpassword",
            is_school=True,
        )
        school_school = School.objects.create(
            user=school,
            name="XYZ School",
            city="City Name",
        )
        form = StudentSignUpForm(
            data={
                "email": "test@example.com",
                "password1": "123123qq",
                "password2": "123123qq",
                "name": "John",
                "surname": "Doe",
                "patronymic": "Smith",
                "school": school_school,
            },
        )
        self.assertTrue(form.is_valid())

    def test_school_signup_form_valid(self):
        form = SchoolSignUpForm(
            data={
                "email": "test@example.com",
                "password1": "123123qq",
                "password2": "123123qq",
                "name": "XYZ School",
                "city": "City Name",
            },
        )
        self.assertTrue(form.is_valid())
