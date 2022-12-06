import pytest
from django.test import Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from pytest_django.asserts import assertTemplateUsed
from profiles.models import Profile


@pytest.mark.django_db
def test_profile_model():
    user = User.objects.create_user(username="TestUser", password="testpassword")
    profile = Profile.objects.create(
        user = user,
    )
    expected_value = "TestUser"

    assert str(profile) == expected_value



def test_profiles_index_url():
    path = reverse("profiles_index")

    assert path == "/profiles/"
    assert resolve(path).view_name == "profiles_index"


@pytest.mark.django_db
def test_profile_url():
    user = User.objects.create_user(username="TestUser", password="testpassword")
    profile = Profile.objects.create(
        user = user,
    )
    path = reverse("profile", args=[profile.user.username])

    assert path == f"/profiles/TestUser/"
    assert resolve(path).view_name == "profile"


@pytest.mark.django_db
def test_profiles_index_view():
    client = Client()
    path = reverse("profiles_index")
    home_path = reverse("index")
    lettings_path = reverse("lettings_index")
    response = client.get(path)
    content = response.content.decode()
    expected_title = "<title>Profiles</title>"

    assert response.status_code == 200
    assert expected_title in content
    assert home_path in content
    assert lettings_path in content
    assertTemplateUsed(response, "profiles/index.html")


@pytest.mark.django_db
def test_profile_view():
    client = Client()
    user = User.objects.create_user(username="TestUser", password="testpassword")
    profile = Profile.objects.create(
        user = user,
    )
    path = reverse("profile", args=[profile.user.username])
    home_path = reverse("index")
    profiles_path = reverse("profiles_index")
    lettings_path = reverse("lettings_index")
    response = client.get(path)
    content = response.content.decode()
    expected_title = f"<title>{profile.user.username}</title>"

    assert response.status_code == 200
    assert expected_title in content
    assert home_path in content
    assert profiles_path in content
    assert lettings_path in content
    assertTemplateUsed(response, "profiles/profile.html")
