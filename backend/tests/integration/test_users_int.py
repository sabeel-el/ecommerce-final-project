import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

# Create a client fixture for the tests
@pytest.fixture
def client():
    return APIClient()

# Create a sample user fixture
@pytest.fixture
def sample_user(db):
    return User.objects.create_user(
        username="testuser@example.com",
        email="testuser@example.com",
        password="testpassword",
    )

# Create an admin user fixture
@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username="admin@example.com",
        email="admin@example.com",
        password="adminpassword",
    )

#  Test user registration
@pytest.mark.django_db
def test_register_user(client):
    url = "/api/users/register/"
    data = {
        "name": "Test User",
        "email": "newuser@example.com",
        "password": "testpassword",
    }
    response = client.post(url, data, format="json")
    assert response.status_code == 200
    assert "token" in response.data

# Test user login
@pytest.mark.django_db
def test_login_user(client, sample_user):
    url = "/api/users/login/"
    data = {
        "username": sample_user.username,
        "password": "testpassword",
    }
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data

# Test get user profile (authenticated)
@pytest.mark.django_db
def test_get_user_profile(client, sample_user):
    client.force_authenticate(user=sample_user)
    url = "/api/users/profile/"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == sample_user.email

# Test get all users (admin only)
@pytest.mark.django_db
def test_get_users_admin(client, admin_user):
    client.force_authenticate(user=admin_user)
    url = "/api/users/"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)

#  Test get user by ID (admin only)
@pytest.mark.django_db
def test_get_user_by_id(client, admin_user, sample_user):
    client.force_authenticate(user=admin_user)
    url = f"/api/users/{sample_user.id}/"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == sample_user.email

#  Test update user (admin only)
# @pytest.mark.django_db
# def test_update_user(client, admin_user, sample_user):
#     client.force_authenticate(user=admin_user)
#     url = f"/api/users/{sample_user.id}/"
#     data = {
#         "name": "Admin Updated Name",
#         "email": "adminupdated@example.com",
#         "isAdmin": True,
#     }
#     response = client.put(url, data, format="json")
#     assert response.status_code == status.HTTP_200_OK
#     updated_user = User.objects.get(id=sample_user.id)
#     assert updated_user.first_name == "Admin Updated Name"
#     assert updated_user.email == "adminupdated@example.com"

# Test delete user (admin only)
# @pytest.mark.django_db
# def test_delete_user(client, admin_user, sample_user):
#     client.force_authenticate(user=admin_user)
#     url = f"/api/users/{sample_user.id}/"
#     response = client.delete(url)
#     assert response.status_code == status.HTTP_204_NO_CONTENT
#     assert not User.objects.filter(id=sample_user.id).exists()
