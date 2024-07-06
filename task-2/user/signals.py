from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from organisation.models import Organisation


User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        organisation = Organisation.objects.create(
            name=f"{instance.firstName}'s Organisation"
        )
        instance.organisations.add(organisation)
        instance.save()
