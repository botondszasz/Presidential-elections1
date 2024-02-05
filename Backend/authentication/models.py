from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

#Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_bio = models.TextField(max_length=500, default="Default description")
    hasVoted = models.BooleanField(default=False)
    votedFor = models.IntegerField(default=None, editable=True, null=True)
    numberOfVotes = models.IntegerField(default=0, editable=True)
    hasApplied = models.BooleanField(default=False)
    linkFacebook = models.TextField(max_length=1000, default="")
    linkInstagram = models.TextField(max_length=1000, default="")
    linkLinkedin = models.TextField(max_length=1000, default="")

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

     


