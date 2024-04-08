from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import CustomUser, School, Student


__all__ = []


class StudentSignUpForm(UserCreationForm):
    name = forms.CharField(
        max_length=100,
        label="Имя",
        required=True,
    )

    surname = forms.CharField(
        max_length=100,
        label="Фамилия",
        required=True,
    )

    patronymic = forms.CharField(
        max_length=100,
        label="Отчество",
    )

    school = forms.ModelChoiceField(
        queryset=School.objects.all(),
        label="Школа",
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            CustomUser.email.field.name,
            "name",
            "surname",
            "patronymic",
            "school",
        )

    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        Student.objects.create(
            user=user,
            name=self.cleaned_data.get("name"),
            surname=self.cleaned_data.get("surname"),
            patronymic=self.cleaned_data.get("patronymic"),
            school=self.cleaned_data.get("school"),
        )
        return user


class SchoolSignUpForm(UserCreationForm):
    name = forms.CharField(
        max_length=255,
        label="Название",
        required=True,
    )

    city = forms.CharField(
        max_length=255,
        label="Город",
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            CustomUser.email.field.name,
            "name",
            "city",
        )

    def save(self):
        user = super().save(commit=False)
        user.is_school = True
        user.save()
        School.objects.create(
            user=user,
            name=self.cleaned_data.get("name"),
            city=self.cleaned_data.get("city"),
        )
        return user
