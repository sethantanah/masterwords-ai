from django.db import models


class Tools(models.Model):
    tool = models.CharField(max_length=200, help_text='tool name')
    url = models.CharField(max_length=50, help_text='url name', blank=True)
    url2 = models.CharField(max_length=50, help_text='url path')
    description = models.TextField(help_text='description')
    stars = models.IntegerField(help_text='stars')
    image = models.CharField(max_length=3000, help_text='image', blank=True)
    ext = models.BooleanField(default=False)

    class Meta:
        ordering = ['-tool']

    def __str__(self):
        return self.tool


class Tones(models.Model):
    tone = models.CharField(max_length=50, help_text='tone')
    icon = models.CharField(max_length=3000, help_text='Icon', blank=True)

    class Meta:
        ordering = ['-tone']

    def __str__(self):
        return self.tone


class Platforms(models.Model):
    platform = models.CharField(max_length=50, help_text='tone')
    icon = models.CharField(max_length=3000, help_text='Icon', blank=True)
    class Meta:
        ordering = ['-platform']

    def __str__(self):
        return self.platform


class PostType(models.Model):
    type = models.CharField(max_length=50, help_text='tone')
    icon = models.CharField(max_length=3000, help_text='Icon', blank=True)
    class Meta:
        ordering = ['-type']

    def __str__(self):
        return self.type
