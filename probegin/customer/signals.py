from django.db.models.signals import post_save
from django.dispatch import receiver
from customer.models import (
    Customer,
    CustomerDiscount,
    ReplicaCustomer,
    ReplicaCustomerDiscount
)


@receiver(post_save, sender=Customer)
def customer(sender, instance, created, using, **kwargs):
    if using == 'default':
        model = ReplicaCustomer
        already_exists = model.objects.filter(
            lCustomer_id=instance.pk
        ).exists()
        if created and not already_exists:
            model.objects.create(
                lCustomer_id=instance.pk,
                cSearchName=instance.search_name,
                cName=instance.name,
                vEmailSender=instance.email_sender
            )
        else:
            model.objects.filter(lCustomer_id=instance.pk).update(
                cSearchName=instance.search_name,
                cName=instance.name,
                vEmailSender=instance.email_sender
            )


@receiver(post_save, sender=CustomerDiscount)
def customer_discount(sender, instance, created, using, **kwargs):
    model = ReplicaCustomerDiscount
    if using == 'default':
        already_exists = model.objects.filter(
            intCustomerDiscountId=instance.pk
        ).exists()
        if created and not already_exists:
            model.objects.create(
                intCustomerDiscountId=instance.pk,
                intCustomerId=instance.customer_id,
                chvDescription=instance.description,
                dtmInsertDate=instance.insert_date
            )
        else:
            model.objects.filter(intCustomerDiscountId=instance.pk).update(
                intCustomerId=instance.customer_id,
                chvDescription=instance.description,
                dtmInsertDate=instance.insert_date
            )
