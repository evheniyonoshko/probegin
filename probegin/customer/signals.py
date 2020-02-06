from django.db.models.signals import post_save
from django.dispatch import receiver
from customer.models import Customer, CustomerDiscount


@receiver(post_save, sender=Customer)
@receiver(post_save, sender=CustomerDiscount)
def save_or_update_objects_in_old_db(sender, instance, created, using, **kwargs):
    if using == 'default':
        if created:
            instance.save(using='old_default', force_insert=True)
        else:
            instance.save(using='old_default')

