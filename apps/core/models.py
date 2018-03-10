from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django_resized import ResizedImageField


class Address(models.Model):
    user = models.OneToOneField(User, related_name='address_user',
                                verbose_name='endereço do usuário',
                                on_delete=models.CASCADE)

    route = models.CharField(_('rua'), max_length=200)
    country = models.CharField(_('pais'), max_length=200)
    administrative_area_level_1 = models.CharField(_('estado'), max_length=200)
    administrative_area_level_2 = models.CharField(_('cidade'), max_length=200)
    street_number = models.CharField(_('número'), max_length=30)
    postal_code = models.CharField(_('CEP'), max_length=20)
    sublocality_level_1 = models.CharField(_('bairro'), max_length=200)
    complement = models.CharField(_('complemento'), max_length=20, blank=True)

    def full_address(self):
        return f'{self.route}, {self.street_number} - {self.sublocality_level_1} - {self.administrative_area_level_2}'

    def __str__(self):
        return self.full_address()

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile',
                                verbose_name='Profile',
                                on_delete=models.CASCADE)

    photo_medium = ResizedImageField(size=[600, 600], crop=['top', 'left'], upload_to='profile_photo/medium', blank=True)
    photo_thumb = ResizedImageField(size=[200, 200], crop=['top', 'left'], upload_to='profile_photo/thumb', blank=True)

    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfils'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Address.objects.create(user=instance)

    instance.user_profile.save()
    instance.address_user.save()
