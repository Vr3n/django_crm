from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Customer

# Create customer profile on creation of user.
def create_customer_profile(sender, instance, created, **kwargs):

    if created:
        group = Group.objects.get(name="customer")
        instance.groups.add(group)

        Customer.objects.create(
            user=instance,
            name=instance.username,
        )
        print('User and Customer Created')

# Connector post_save to create_customer_profile when User model is triggered.
post_save.connect(create_customer_profile, sender=User)


# Updating the customer on updation of user.
def update_customer_profile(sender, instance, created, **kwrags):

    if created == False:
        instance.customer.name = instance.username
        instance.customer.save()
        print('User and Customer Updated')

# Connector post_save to update_customer_profile when User model is triggered.
post_save.connect(update_customer_profile, sender=User)