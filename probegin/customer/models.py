from django.db import models


class Customer(models.Model):
    lCustomer_id = models.AutoField(primary_key=True)
    cSearchName = models.TextField()
    cName = models.CharField(max_length=100)             # max_length was changed because old database has values more than 10
    vEmailSender = models.CharField(max_length=255)

    class Meta:
        db_table = "CUSTOMER"


class CustomerDiscount(models.Model):
    intCustomerDiscountId = models.AutoField(primary_key=True)
    intCustomer = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='intCustomerId')
    chvDescription = models.CharField(max_length=100)     # max_length was changed because old database has values more than 50
    dtmInsertDate = models.DateTimeField()

    class Meta:
        db_table = "CUSTOMER_DISCOUNT"