from django.db.models.query import QuerySet

from customer import models


class ReplicaCustomerQuerySet(QuerySet):
    def diff(self):
        existing_obj_ids = list(
            models.Customer.objects.values_list('id', flat=True)
        )
        return self.exclude(lCustomer_id__in=existing_obj_ids)


class ReplicaCustomerDiscountQuerySet(QuerySet):
    def diff(self):
        existing_obj_ids = list(
            models.CustomerDiscount.objects.values_list('id', flat=True)
        )
        return self.exclude(intCustomerDiscountId__in=existing_obj_ids)
