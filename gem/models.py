from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from gem.constants import GENDERS
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.wagtailadmin.edit_handlers import FieldPanel


class GemUserProfile(models.Model):
    user = models.OneToOneField(
        User, related_name="gem_profile", primary_key=True)

    gender = models.CharField(
        max_length=1, choices=GENDERS, blank=True, null=True)


@receiver(post_save, sender=User)
def gem_user_profile_handler(sender, instance, created, **kwargs):
    if created:
        profile = GemUserProfile(user=instance)
        profile.save()


@register_setting
class SiteSettings(BaseSetting):
    comment_filters = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL)

    banned_keywords_and_patterns = models.TextField(
        verbose_name='Banned Keywords and Patterns',
        null=True,
        blank=True,
        help_text="Banned keywords and patterns for comments, "
                  "separated by a line a break."
    )

    panels = [
        FieldPanel('banned_keywords_and_patterns'),
    ]
