import pytest
import pytz
from datetime import datetime, timedelta

from .models import (
    Customer,
    CustomerDiscount,
    ReplicaCustomer,
    ReplicaCustomerDiscount
)


@pytest.fixture
def customer_data():
    return {
        'search_name': 'test',
        'name': 'test',
        'email_sender': 'test@gmail.com',
    }


@pytest.fixture
def customer(customer_data):
    return Customer.objects.create(**customer_data)


@pytest.fixture
def customer_discount_data(customer):
    return {
        'customer_id': customer.pk,
        'description': 'test description',
        'insert_date': datetime.utcnow().replace(tzinfo=pytz.utc),
    }


@pytest.fixture
def customer_discount(customer_discount_data):
    return CustomerDiscount.objects.create(**customer_discount_data)


@pytest.mark.django_db
def test_create_customer(customer_data):
    obj = Customer.objects.create(**customer_data)
    assert ReplicaCustomer.objects.filter(lCustomer_id=obj.pk).exists()
    obj = ReplicaCustomer.objects.get(lCustomer_id=obj.pk)
    assert customer_data.get('search_name') == obj.cSearchName
    assert customer_data.get('name') == obj.cName
    assert customer_data.get('email_sender') == obj.vEmailSender


@pytest.mark.django_db
def test_update_customer(customer_data, customer):
    customer.search_name = 'new test'
    customer.name = 'new test'
    customer.email_sender = 'new@gmail.com'
    customer.save()
    assert ReplicaCustomer.objects.filter(lCustomer_id=customer.pk).exists()
    obj = ReplicaCustomer.objects.get(pk=customer.pk)
    assert obj.cSearchName == 'new test' == customer.search_name
    assert obj.cName == 'new test' == customer.name
    assert obj.vEmailSender == 'new@gmail.com' == customer.email_sender


@pytest.mark.django_db
def test_create_customer_discount(customer_discount_data):
    obj = CustomerDiscount.objects.create(**customer_discount_data)
    assert ReplicaCustomerDiscount.objects.filter(
        intCustomerDiscountId=obj.pk
    ).exists()
    obj = ReplicaCustomerDiscount.objects.get(
        intCustomerDiscountId=obj.pk
    )
    assert customer_discount_data.get('customer_id') == obj.intCustomerId
    assert customer_discount_data.get('description') == obj.chvDescription
    assert customer_discount_data.get('insert_date') == obj.dtmInsertDate


@pytest.mark.django_db
def test_update_customer_discount(customer_discount):
    now = datetime.utcnow().replace(tzinfo=pytz.utc)
    customer_discount.description = 'new description'
    customer_discount.insert_date = now - timedelta(hours=1)
    customer_discount.save()
    assert ReplicaCustomerDiscount.objects.filter(
        intCustomerDiscountId=customer_discount.pk
    ).exists()
    obj = ReplicaCustomerDiscount.objects.get(
        intCustomerDiscountId=customer_discount.pk
    )
    assert obj.chvDescription == customer_discount.description
    assert obj.dtmInsertDate == customer_discount.insert_date



