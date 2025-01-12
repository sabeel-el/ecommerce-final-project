import pytest
from base.models import Product, Review, Order, OrderItem, ShippingAddress
from django.contrib.auth.models import User
from django import forms
from django.urls import reverse


# Helper fixture to create a test user
@pytest.fixture
def test_user(db):
    return User.objects.create_user(username="testuser", password="testpassword")

@pytest.fixture
def sample_product(test_user):
    return Product.objects.create(
        user=test_user,
        name="Product Name",
        price=0,
        brand="Sample brand",
        countInStock=0,
        category="Sample category",
        description=" "
    )

@pytest.mark.django_db
def test_product_creation(sample_product):
  p = sample_product
  assert isinstance(p, Product) is True
  assert p.name == "Product Name"

# ✅ Unit Test for Product Model
def test_product_str(sample_product):
    # Fix the assertion to reflect the actual product attributes
    assert str(sample_product) == "Product Name | Sample brand | 0"

# ✅ Unit Test for Review Model
def test_review_str(test_user, sample_product):
    review = Review.objects.create(
        product=sample_product,
        user=test_user,
        rating=5,
        comment="Great product"
    )
    # Fix the assertion to match review rating
    assert str(review) == "5"

# ✅ Unit Test for Order Model
def test_order_str(test_user):
    order = Order.objects.create(user=test_user)
    assert str(order) == str(order.createdAt)

# ✅ Unit Test for OrderItem Model
def test_order_item_str(sample_product):
    order_item = OrderItem.objects.create(
        product=sample_product,
        name=sample_product.name,
        qty=2,
        price=50.00
    )
    # Fix the assertion to match product name
    assert str(order_item) == "Product Name"

# ✅ Unit Test for ShippingAddress Model
@pytest.mark.django_db
def test_shipping_address_str(test_user):
    order = Order.objects.create(user=test_user)  
    shipping_address = ShippingAddress.objects.create(
        order=order,
        address="123 Main St"
    )
    assert str(shipping_address) == "123 Main St"



def test_product_url():
    url = reverse('create_product')
    assert  'create/' in url  