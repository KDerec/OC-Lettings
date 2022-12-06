import pytest
from django.test import Client
from django.urls import reverse, resolve
from pytest_django.asserts import assertTemplateUsed
from lettings.models import Address, Letting


@pytest.mark.django_db
def test_address_model():
    address = Address.objects.create(
        number=1600,
        street="Pennsylvania Avenue NW",
        city="Washington",
        state="DC",
        zip_code=20500,
        country_iso_code="USA",
    )
    expected_value = "1600 Pennsylvania Avenue NW"

    assert str(address) == expected_value


@pytest.mark.django_db
def test_letting_model():
    address = Address.objects.create(
        number=1600,
        street="Pennsylvania Avenue NW",
        city="Washington",
        state="DC",
        zip_code=20500,
        country_iso_code="USA",
    )
    letting = Letting.objects.create(title="White House", address=address)
    expected_value = "White House"

    assert str(letting) == expected_value


def test_lettings_index_url():
    path = reverse("lettings_index")

    assert path == "/lettings/"
    assert resolve(path).view_name == "lettings_index"


@pytest.mark.django_db
def test_letting_url():
    address = Address.objects.create(
        number=1600,
        street="Pennsylvania Avenue NW",
        city="Washington",
        state="DC",
        zip_code=20500,
        country_iso_code="USA",
    )
    letting = Letting.objects.create(title="White House", address=address)
    path = reverse("letting", args=[letting.id])

    assert path == f"/lettings/{letting.id}/"
    assert resolve(path).view_name == "letting"


@pytest.mark.django_db
def test_lettings_index_view():
    client = Client()
    path = reverse("lettings_index")
    home_path = reverse("index")
    profiles_path = reverse("profiles_index")
    response = client.get(path)
    content = response.content.decode()
    expected_title = "<title>Lettings</title>"

    assert response.status_code == 200
    assert expected_title in content
    assert home_path in content
    assert profiles_path in content
    assertTemplateUsed(response, "lettings/index.html")


@pytest.mark.django_db
def test_letting_view():
    client = Client()
    address = Address.objects.create(
        number=1600,
        street="Pennsylvania Avenue NW",
        city="Washington",
        state="DC",
        zip_code=20500,
        country_iso_code="USA",
    )
    letting = Letting.objects.create(title="White House", address=address)
    path = reverse("letting", args=[letting.id])
    home_path = reverse("index")
    profiles_path = reverse("profiles_index")
    lettings_path = reverse("lettings_index")
    response = client.get(path)
    content = response.content.decode()
    expected_title = "<title>White House</title>"

    assert response.status_code == 200
    assert expected_title in content
    assert home_path in content
    assert profiles_path in content
    assert lettings_path in content
    assertTemplateUsed(response, "lettings/letting.html")
