import pytest
from django.test import Client
from django.urls import reverse, resolve
from pytest_django.asserts import assertTemplateUsed
from profiles.models import Profile


@pytest.mark.django_db
def test_profile_model(test_user):
    user = test_user
    profile = Profile.objects.create(
        user=user,
    )
    expected_value = "TestUser"

    assert str(profile) == expected_value


def test_profiles_index_url(reverse_paths):
    assert reverse_paths["profiles"] == "/profiles/"
    assert resolve(reverse_paths["profiles"]).view_name == "profiles_index"


@pytest.mark.django_db
def test_profile_url(test_user):
    user = test_user
    profile = Profile.objects.create(
        user=user,
    )
    path = reverse("profile", args=[profile.user.username])

    assert path == f"/profiles/TestUser/"
    assert resolve(path).view_name == "profile"


@pytest.mark.django_db
def test_profiles_index_view(reverse_paths):
    client = Client()
    response = client.get(reverse_paths["profiles"])
    content = response.content.decode()
    expected_title = "<title>Profiles</title>"

    assert response.status_code == 200
    assert expected_title in content
    assert reverse_paths["home"] in content
    assert reverse_paths["lettings"] in content
    assertTemplateUsed(response, "profiles/index.html")


@pytest.mark.django_db
def test_profile_view(test_user, reverse_paths):
    client = Client()
    user = test_user
    profile = Profile.objects.create(
        user=user,
    )
    path = reverse("profile", args=[profile.user.username])
    response = client.get(path)
    content = response.content.decode()
    expected_title = f"<title>{profile.user.username}</title>"

    assert response.status_code == 200
    assert expected_title in content
    assert reverse_paths["home"] in content
    assert reverse_paths["lettings"] in content
    assert reverse_paths["profiles"] in content
    assertTemplateUsed(response, "profiles/profile.html")
