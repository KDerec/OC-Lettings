import pytest
from django.test import Client
from django.urls import reverse, resolve
from pytest_django.asserts import assertTemplateUsed
from lettings.models import Letting


@pytest.mark.django_db
def test_address_model(test_address):
    address = test_address
    expected_value = "1600 Pennsylvania Avenue NW"

    assert str(address) == expected_value


@pytest.mark.django_db
def test_letting_model(test_address):
    address = test_address
    letting = Letting.objects.create(title="White House", address=address)
    expected_value = "White House"

    assert str(letting) == expected_value


def test_lettings_index_url(reverse_paths):
    assert reverse_paths["lettings"] == "/lettings/"
    assert resolve(reverse_paths["lettings"]).view_name == "lettings_index"


@pytest.mark.django_db
def test_letting_url(test_address):
    address = test_address
    letting = Letting.objects.create(title="White House", address=address)
    path = reverse("letting", args=[letting.id])

    assert path == f"/lettings/1/"
    assert resolve(path).view_name == "letting"


@pytest.mark.django_db
def test_lettings_index_view(reverse_paths):
    client = Client()
    response = client.get(reverse_paths["lettings"])
    content = response.content.decode()
    expected_title = "<title>Lettings</title>"

    assert response.status_code == 200
    assert expected_title in content
    assert reverse_paths["home"] in content
    assert reverse_paths["profiles"] in content
    assertTemplateUsed(response, "lettings/index.html")


@pytest.mark.django_db
def test_letting_view(test_address, reverse_paths):
    client = Client()
    address = test_address
    letting = Letting.objects.create(title="White House", address=address)
    path = reverse("letting", args=[letting.id])
    response = client.get(path)
    content = response.content.decode()
    expected_title = "<title>White House</title>"

    assert response.status_code == 200
    assert expected_title in content
    assert reverse_paths["home"] in content
    assert reverse_paths["lettings"] in content
    assert reverse_paths["profiles"] in content
    assertTemplateUsed(response, "lettings/letting.html")
