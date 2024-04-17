from cities_light.models import City
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import widgets
from django_recaptcha.fields import ReCaptchaField

from users.models import CustomUser, School, Student


__all__ = []


class StylesFormMixin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            if field.html_name != "captcha":
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
    captcha = ReCaptchaField()


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

    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        to_field_name="id",
        label="Город",
        empty_label="Выберите город",
        required=True,
        widget=widgets.Select(
            attrs={
                "placeholder": "Город",
                "hx-get": "/auth/load_schools/",
                "hx-target": "#id_school",
            },
        ),
    )

    school = forms.ModelChoiceField(
        queryset=School.objects.none(),
        label="Школа",
        empty_label="Выберите школу",
        required=True,
        widget=widgets.Select(
            attrs={
                "placeholder": "Школа",
            },
        ),
    )

    captcha = ReCaptchaField()

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            CustomUser.email.field.name,
            "name",
            "surname",
            "patronymic",
            "city",
            "school",
            "captcha",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "city" in self.data:
            city_id = int(self.data.get("city"))
            self.fields["school"].queryset = School.objects.filter(city_id=city_id)

    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        Student.objects.create(
            user=user,
            name=self.cleaned_data.get("name"),
            surname=self.cleaned_data.get("surname"),
            patronymic=self.cleaned_data.get("patronymic"),
            city=self.cleaned_data.get("city"),
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

    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        label="Город",
        empty_label="Выберите город",
        required=True,
        widget=widgets.Select(
            attrs={"placeholder": "Город"},
        ),
    )

    captcha = ReCaptchaField()

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            CustomUser.email.field.name,
            "name",
            "city",
            "captcha",
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
