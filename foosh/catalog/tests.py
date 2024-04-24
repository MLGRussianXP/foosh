from cities_light.models import City
from django.contrib.auth import get_user_model
from django.core import management
from django.test import Client, TestCase
from django.urls import reverse

from catalog.models import Category, Item
from users.models import School, Student


__all__ = []


def setUpModule():
    management.call_command(
        "cities_light_fixtures",
        "load",
        base_url="file:fixtures/cities_light/",
    )


class CatalogViewTests(TestCase):
    def setUp(self):
        user = get_user_model()

        self.city = City.objects.get(name="Moscow")

        school = user.objects.create_user(
            email="testschool@ya.ru",
            password="123123qq",
            is_school=True,
        )
        self.school = School.objects.create(
            user=school,
            name="XYZ School",
            city=self.city,
        )

        self.user = user.objects.create_user(
            email="testuser@ya.ru",
            password="123123qq",
        )
        self.student = Student.objects.create(
            user=self.user,
            name="John",
            surname="Doe",
            patronymic="Smith",
            city=self.city,
            school=self.school,
        )

        self.item1 = Item.objects.create(
            name="Пицца",
            description="Пицца черепашек ниндзя!",
            price=69.90,
            category=Category.BAKERY,
            school=self.school,
        )
        self.item2 = Item.objects.create(
            name="Добри кола",
            description="ммммм...",
            price=49.90,
            category=Category.DRINKS,
            school=self.school,
        )
        self.client = Client()

    def test_item_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(
                "catalog:category",
                kwargs={
                    "category": Category.BAKERY,
                },
            ),
        )

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["items"],
            [self.item1],
        )

    def test_item_detail_view(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(
                "catalog:item",
                kwargs={
                    "pk": self.item1.pk,
                },
            ),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["item"], self.item1)

    def test_no_category_redirect_view(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("catalog:redirect"),
        )

        self.assertRedirects(
            response,
            reverse(
                "catalog:category",
                kwargs={
                    "category": Category.BAKERY,
                },
            ),
        )

    def test_redirect_to_login_view(self):
        self.client.logout()
        response = self.client.get(
            reverse(
                "catalog:category",
                kwargs={
                    "category": Category.BAKERY,
                },
            ),
        )

        expected_url = reverse("users:login")
        expected_url += "?next=" + reverse(
            "catalog:category",
            kwargs={
                "category": Category.BAKERY,
            },
        )

        self.assertRedirects(
            response,
            expected_url,
        )
