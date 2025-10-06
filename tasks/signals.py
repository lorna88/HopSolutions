from django.db.models.signals import post_save
from django.dispatch import receiver

from tags.models import Tag
from tasks.models import Category
from users.models import User


@receiver(post_save, sender=User)
def create_default_settings(sender, instance, created, **kwargs):
    """
    Creates default tags and categories after a new user was registered.
    This is need because every user has his own tasks, categories and tags.
    """
    if created:
        categories = [
            Category(name="Today", slug=f"today-{instance.username}", user=instance),
            Category(name="Tomorrow", slug=f"tomorrow-{instance.username}", user=instance),
            Category(name="Nearest time", slug=f"nearest-time-{instance.username}", user=instance),
        ]
        Category.objects.bulk_create(categories)

        tags = [
            Tag(name="Important", slug=f"important-{instance.username}", color="--background-yellow", user=instance),
            Tag(name="Deadline", slug=f"deadline-{instance.username}", color="--background-pink", user=instance),
            Tag(name="Family", slug=f"family-{instance.username}", color="--background-green", user=instance),
        ]
        Tag.objects.bulk_create(tags)