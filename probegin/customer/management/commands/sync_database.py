from django.db import connection
from django.db.models import Q
from django.core.management.color import no_style
from django.core.management.base import BaseCommand, CommandError

from customer.models import (
    Customer,
    CustomerDiscount,
    ReplicaCustomer,
    ReplicaCustomerDiscount
)


class Command(BaseCommand):
    help = 'Management command to import all the data from old db into new one'

    def handle(self, *args, **options):
        replica_customers = ReplicaCustomer.objects.diff()
        customer_objs = [
            Customer(
                id=obj.lCustomer_id,
                search_name=obj.cSearchName,
                name=obj.cName,
                email_sender=obj.vEmailSender
            )
            for obj in replica_customers
        ]
        Customer.objects.bulk_create(customer_objs)

        replica_customer_discounts = ReplicaCustomerDiscount.objects.diff()
        customer_discount_objs = [
            CustomerDiscount(
                id=obj.intCustomerDiscountId,
                customer_id=obj.intCustomerId,
                description=obj.chvDescription,
                insert_date=obj.dtmInsertDate
            )
            for obj in replica_customer_discounts
        ]
        CustomerDiscount.objects.bulk_create(customer_discount_objs)
