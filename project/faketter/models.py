from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class Feek(models.Model):
    user = models.ForeignKey(User, related_name="feeks", on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="feek_like", blank=True)

    # keep track ro count of likes
    def number_of_likes(self):
        return self.likes.count()

    def __str__(self) -> str:
        return f"{self.user} ({self.created_at:%Y-%m-%d %H:%M}) {self.body}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self", related_name="follow_by", symmetrical=False, blank=True
    )
    date_modified = models.DateTimeField(User, auto_now=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    profile_bio = models.CharField(null=True, blank=True, max_length=500)
    personal_link = models.CharField(null=True, blank=True, max_length=100)
    facebook_link = models.CharField(null=True, blank=True, max_length=100)
    instagram_link = models.CharField(null=True, blank=True, max_length=100)
    linkedin_link = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.user.username


# crear Profile cuando se crea un nuevo usuario


def crear_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        # que el usuario se siga a si mismo
        user_profile.follows.set([instance.profile.id])
        user_profile.save()


post_save.connect(crear_profile, sender=User)
