from django.db import models

from .managers import ReplicaCustomerQuerySet, ReplicaCustomerDiscountQuerySet


class Customer(models.Model):
    search_name = models.TextField()
    name = models.CharField(max_length=100)
    email_sender = models.CharField(max_length=255)


class CustomerDiscount(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    insert_date = models.DateTimeField()


class ReplicaCustomer(models.Model):
    lCustomer_id = models.AutoField(primary_key=True)
    cSearchName = models.TextField()
    cName = models.CharField(max_length=100)
    vEmailSender = models.CharField(max_length=255)

    objects = ReplicaCustomerQuerySet.as_manager()

    class Meta:
        db_table = "CUSTOMER"


class ReplicaCustomerDiscount(models.Model):
    intCustomerDiscountId = models.AutoField(primary_key=True)
    intCustomerId = models.IntegerField()
    chvDescription = models.CharField(max_length=100)
    dtmInsertDate = models.DateTimeField()

    objects = ReplicaCustomerDiscountQuerySet.as_manager()
    
    class Meta:
        db_table = "CUSTOMER_DISCOUNT"
