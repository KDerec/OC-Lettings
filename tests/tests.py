from django.test import Client
from django.urls import reverse, resolve
from pytest_django.asserts import assertTemplateUsed


def test_index_url(reverse_paths):
    assert reverse_paths["home"] == "/"
    assert resolve(reverse_paths["home"]).view_name == "index"


def test_index_view():
    client = Client()
    path = reverse("index")
    profiles_path = reverse("profiles_index")
    lettings_path = reverse("lettings_index")
    response = client.get(path)
    content = response.content.decode()
    expected_title = "<title>Holiday Homes</title>"

    assert response.status_code == 200
    assert expected_title in content
    assert profiles_path in content
    assert lettings_path in content
    assertTemplateUsed(response, "index.html")
