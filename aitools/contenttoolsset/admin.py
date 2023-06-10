from django.contrib import admin

from .models import Tools, Platforms, PostType, Tones

admin.site.register(Tools)
admin.site.register(Platforms)
admin.site.register(PostType)
admin.site.register(Tones)