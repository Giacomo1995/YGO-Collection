from django.db import models
import copy


class UserSet(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)
    collected = models.IntegerField(default=0)
    missing = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Card(models.Model):
    userset = models.ForeignKey(UserSet, on_delete=models.CASCADE)
    collected = models.BooleanField(default=False)
    cardid = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, blank=True)
    desc = models.TextField(blank=True)
    attack = models.IntegerField(null=True, blank=True)
    defence = models.IntegerField(null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)
    attribute = models.CharField(max_length=100, blank=True)
    cardsetname = models.TextField(blank=True)
    cardsetcode = models.CharField(max_length=100, blank=True)
    cardsetrarity = models.CharField(max_length=100, blank=True)
    cardsetraritycode = models.CharField(max_length=100, blank=True)
    image_url = models.TextField(blank=True)
    image_url_small = models.TextField(blank=True)
    image = models.FileField(upload_to='images/', null=True, blank=True, verbose_name="")
    image_small = models.FileField(upload_to='images/', null=True, blank=True, verbose_name="")

    def __str__(self):
        return self.name

    def copy(self):
        return copy.deepcopy(self)

    class Meta:
        ordering = ('name',)
