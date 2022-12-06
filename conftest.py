import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from lettings.models import Address


@pytest.fixture
def test_address():
    address = Address.objects.create(
        number=1600,
        street="Pennsylvania Avenue NW",
        city="Washington",
        state="DC",
        zip_code=20500,
        country_iso_code="USA",
    )

    return address


@pytest.fixture
def test_user():
    user = User.objects.create_user(username="TestUser", password="testpassword")

    return user


@pytest.fixture
def reverse_paths():
    paths = {
        "home": reverse("index"),
        "lettings": reverse("lettings_index"),
        "profiles": reverse("profiles_index"),
    }

    return paths
