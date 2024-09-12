from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} Profile"

    @property
    def followers(self):
        return Follow.objects.filter(follow_user=self.user).count()

    @property
    def following(self):
        return Follow.objects.filter(user=self.user).count()

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save()


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Follow(models.Model):
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    follow_user = models.ForeignKey(
        User, related_name="follow_user", on_delete=models.CASCADE
    )
    date = models.DateTimeField(auto_now_add=True)
