from django.db.models.signals import post_save
from django.dispatch import receiver

from tags.models import Tag
from tasks.models import Category
from users.models import User


@receiver(post_save, sender=User)
def create_default_settings(
        sender: User.__class__,
        instance: User,
        created: bool, **kwargs) -> None:
    """
    Creates default tags and categories after a new user was registered.
    This is need because every user has his own tasks, categories and tags.
    """
    if created:
        categories = [
            Category(name="Today", slug=f"today", user=instance),
            Category(name="Tomorrow", slug=f"tomorrow", user=instance),
            Category(name="Nearest time", slug=f"nearest-time", user=instance),
        ]
        Category.objects.bulk_create(categories)

        tags = [
            Tag(
                name="Important",
                color="--background-yellow",
                user=instance),
            Tag(
                name="Deadline",
                color="--background-pink",
                user=instance),
            Tag(
                name="Family",
                color="--background-green",
                user=instance),
        ]
        Tag.objects.bulk_create(tags)
