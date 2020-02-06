import pytest
import pytz
from datetime import datetime, timedelta

from .models import Customer, CustomerDiscount


@pytest.fixture
def customer_data():
    return {
        'cSearchName': 'test',
        'cName': 'test',
        'vEmailSender': 'test@gmail.com',
    }


@pytest.fixture
def customer(customer_data):
    return Customer.objects.create(**customer_data)

@pytest.fixture
def customer_discount_data(customer):
    return {
        'intCustomer_id': customer.pk,
        'chvDescription': 'test description',
        'dtmInsertDate': datetime.utcnow().replace(tzinfo=pytz.utc),
    }


@pytest.fixture
def customer_discount(customer_discount_data):
    return CustomerDiscount.objects.create(**customer_discount_data)


@pytest.mark.django_db
def test_create_customer(customer_data):
    obj = Customer.objects.create(**customer_data)
    assert Customer.objects.using('old_default').filter(pk=obj.pk).exists()
    old_db_obj = Customer.objects.using('old_default').get(pk=obj.pk)
    assert customer_data.get('cSearchName') == old_db_obj.cSearchName
    assert customer_data.get('cName') == old_db_obj.cName
    assert customer_data.get('vEmailSender') == old_db_obj.vEmailSender


@pytest.mark.django_db
def test_update_customer(customer_data, customer):
    customer.cSearchName = 'new test'
    customer.cName = 'new test'
    customer.vEmailSender = 'new@gmail.com'
    customer.save()
    assert Customer.objects.using('old_default').filter(pk=customer.pk).exists()
    old_db_obj = Customer.objects.using('old_default').get(pk=customer.pk)
    assert old_db_obj.cSearchName == 'new test' == customer.cSearchName
    assert old_db_obj.cName == 'new test' == customer.cName
    assert old_db_obj.vEmailSender == 'new@gmail.com'  == customer.vEmailSender


@pytest.mark.django_db
def test_create_customer_discount(customer_discount_data):
    obj = CustomerDiscount.objects.create(**customer_discount_data)
    assert CustomerDiscount.objects.using('old_default').filter(pk=obj.pk).exists()
    old_db_obj = CustomerDiscount.objects.using('old_default').get(pk=obj.pk)
    assert customer_discount_data.get('intCustomer_id') == old_db_obj.intCustomer_id
    assert customer_discount_data.get('chvDescription') == old_db_obj.chvDescription
    assert customer_discount_data.get('dtmInsertDate') == old_db_obj.dtmInsertDate


@pytest.mark.django_db
def test_update_customer_discount(customer_discount):
    customer_discount.chvDescription = 'new description'
    customer_discount.dtmInsertDate = datetime.utcnow().replace(tzinfo=pytz.utc) - timedelta(hours=1)
    customer_discount.save()
    assert CustomerDiscount.objects.using('old_default').filter(pk=customer_discount.pk).exists()
    old_db_obj = CustomerDiscount.objects.using('old_default').get(pk=customer_discount.pk)
    assert old_db_obj.chvDescription == customer_discount.chvDescription
    assert old_db_obj.dtmInsertDate == customer_discount.dtmInsertDate
