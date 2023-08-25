from cart.models import Cart
from account.models import UserData
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=UserData)
def create_cart(sender, instance, created, **kwargs):
    if created:
        print("------------------------------------")
        print(created)
        print("------------------------------------")
        Cart.objects.create(username=instance.username)

