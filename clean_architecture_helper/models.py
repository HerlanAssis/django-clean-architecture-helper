from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class BaseQuerySet(models.QuerySet):
    def actives(self):
        return self.filter(deleted_at=None)

    def inactives(self):
        return self.exclude(deleted_at=None)


class BaseManager(models.Manager):
    def get_queryset(self):
        return BaseQuerySet(self.model, using=self._db)

    def actives(self):
        return self.get_queryset().actives()

    def inactives(self):
        return self.get_queryset().inactives()


class BaseModel(models.Model):
    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']

    created_at = models.DateTimeField(
        _("Criado às"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("Atualizado às"),
        auto_now=True
    )
    deleted_at = models.DateTimeField(
        _("Deletado às"),
        editable=False,
        blank=True,
        null=True
    )

    def inactive(self):
        self.deleted_at = timezone.now()
        self.save()

    def active(self):
        self.deleted_at = None
        self.save()

    objects = BaseManager()
