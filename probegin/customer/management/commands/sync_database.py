from django.db import connection
from django.db.models import Q
from django.core.management.color import no_style
from django.core.management.base import BaseCommand, CommandError

from customer.models import Customer, CustomerDiscount


class Command(BaseCommand):
    help = 'Management command to import all the data from old db into new one'

    def handle(self, *args, **options):
        customers_exclude_query = Q(lCustomer_id__in=list(Customer.objects.values_list('lCustomer_id', flat=True)))
        old_customer_objects = Customer.objects.using('old_default').exclude(customers_exclude_query)
        customer_objs = [
            Customer(
                lCustomer_id=obj.lCustomer_id,
                cSearchName=obj.cSearchName,
                cName=obj.cName,
                vEmailSender=obj.vEmailSender
            )
            for obj in old_customer_objects
        ]
        Customer.objects.bulk_create(customer_objs)

        customer_discounts_exclude_query = Q(intCustomerDiscountId__in=list(CustomerDiscount.objects.values_list('intCustomerDiscountId', flat=True)))
        old_customer_discount_objects = CustomerDiscount.objects.using('old_default').exclude(customer_discounts_exclude_query)
        customer_discount_objs = [
            CustomerDiscount(
                intCustomerDiscountId=obj.intCustomerDiscountId,
                intCustomer_id=obj.intCustomer_id,
                chvDescription=obj.chvDescription,
                dtmInsertDate=obj.dtmInsertDate
            )
            for obj in old_customer_discount_objects
        ]
        CustomerDiscount.objects.bulk_create(customer_discount_objs)

        sequence_sql = connection.ops.sequence_reset_sql(no_style(), [Customer, CustomerDiscount])
        with connection.cursor() as cursor:
            for sql in sequence_sql:
                cursor.execute(sql)