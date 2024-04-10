from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import widgets

from users.models import CustomUser, School, Student


__all__ = []


class StylesFormMixin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "input"


class CustomAuthForm(AuthenticationForm):
    username = forms.EmailField(
        widget=widgets.EmailInput(attrs={"placeholder": "Почта"}),
    )
    password = forms.CharField(
        widget=widgets.PasswordInput(
            attrs={"placeholder": "Пароль"},
        ),
    )


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        widget=widgets.EmailInput(attrs={"placeholder": "Почта"}),
    )
    password1 = forms.CharField(
        widget=widgets.PasswordInput(attrs={"placeholder": "Пароль"}),
    )
    password2 = forms.CharField(
        widget=widgets.PasswordInput(
            attrs={"placeholder": "Повторите пароль"},
        ),
    )


class StudentSignUpForm(StylesFormMixin, CustomUserCreationForm):
    name = forms.CharField(
        max_length=100,
        label="Имя",
        required=True,
        widget=widgets.TextInput(
            attrs={"placeholder": "Имя"},
        ),
    )

    surname = forms.CharField(
        max_length=100,
        label="Фамилия",
        required=True,
        widget=widgets.TextInput(
            attrs={"placeholder": "Фамилия"},
        ),
    )

    patronymic = forms.CharField(
        max_length=100,
        label="Отчество",
        widget=widgets.TextInput(
            attrs={"placeholder": "Отчество"},
        ),
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


class SchoolSignUpForm(StylesFormMixin, CustomUserCreationForm):
    name = forms.CharField(
        max_length=255,
        label="Название",
        required=True,
        widget=widgets.TextInput(
            attrs={"placeholder": "Название"},
        ),
    )

    city = forms.CharField(
        max_length=255,
        label="Город",
        required=True,
        widget=widgets.TextInput(
            attrs={"placeholder": "Город"},
        ),
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
