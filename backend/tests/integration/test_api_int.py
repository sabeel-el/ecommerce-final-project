# import pytest
# # @pytest.mark.django_db
# # def test_product_created():
# #   Product.objects.create
# from rest_framework.reverse import reverse
# from rest_framework.test import APIClient
# from base.models import Product


# def create_product():
#   return Product.objects.create(
#         name=" Product Name ",
#         price=0,
#         brand="Sample brand ",
#         countInStock=0,
#         category="Sample category",
#         description=" ")

# @pytest.mark.django_db
# def test_product_creation():
#   p = create_product()
#   assert isinstance(p, Product) is True
#   assert p.name == " Product Name "

# # Api test  - Integration testing
# def test_api_product_creation():
#     client = APIClient()
#     response = client.post("/api/products/create/")
#     assert response.status_code == 200

import pytest
from rest_framework import status
from base.models import Product
from django.contrib.auth.models import User
from rest_framework.test import APIClient



@pytest.fixture
def sample_product():
    return Product.objects.create(
        user= User.objects.create_user(username="testuser", password="testpassword"),
        name="Product Name",
        price=0.00,
        brand="Sample brand",
        countInStock=0,
        category="Sample category",
        description=" "
    )

@pytest.mark.django_db
def test_get_products(client):
    url = '/api/products/'
    response = client.get(url, {'page': 1, 'keyword': 'Product'})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert 'products' in data
    assert isinstance(data['products'], list)
    assert 'page' in data
    assert 'pages' in data

@pytest.mark.django_db
def test_get_top_products(client):
    url = '/api/products/top/'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5
    assert all('rating' in product for product in data)

@pytest.mark.django_db
def test_get_product(client, sample_product):
    url = f'/api/products/{sample_product._id}/'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['name'] == sample_product.name

# @pytest.mark.django_db
# def test_create_product(admin_user):
#     url = '/api/products/create/'
#     client=APIClient()
#     client.force_authenticate(user=admin_user)
#     data = {
#         'name': 'New Product',
#         'price': 20.00,
#         'brand': 'Brand Name',
#         'countInStock': 100,
#         'category': 'Category',
#         'description': 'Product description'
#     }
#     response = client.post(url, data, format='json')
#     assert response.status_code == 200
#     created_product = response.json()
#     assert 'name' in created_product
#     assert created_product['name'] == data['name']

@pytest.mark.django_db
def test_update_product(client, admin_user, sample_product):
    url = f'/api/products/update/{sample_product._id}/'
    client=APIClient()
    client.force_authenticate(user=admin_user)
    data = {
        'name': 'Updated Product',
        'price': 25.0,
        'brand': 'Updated Brand',
        'countInStock': 120,
        'category': 'Updated Category',
        'description': 'Updated description'
    }
    response = client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    updated_product = response.json()
    assert updated_product['name'] == data['name']
    assert updated_product['countInStock'] == (data['countInStock'])

@pytest.mark.django_db
def test_delete_product(client, admin_user, sample_product):
    url = f'/api/products/delete/{sample_product._id}/'
    client=APIClient()
    client.force_authenticate(user=admin_user)
    response = client.delete(url)
    assert response.status_code == 200
    assert not Product.objects.filter(_id=sample_product._id).exists()

@pytest.mark.django_db
def test_create_product_review(client, sample_product):
    url = f'/api/products/{sample_product._id}/reviews/'
    client=APIClient()
    client.force_authenticate(user= User.objects.create_user(username="testuser1", password="testpassword"))
    data = {
        'rating': 5,
        'comment': 'Great product!'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    reviews = sample_product.review_set.all()
    assert len(reviews) == 1
    assert reviews[0].rating == 5
    assert reviews[0].comment == 'Great product!'
