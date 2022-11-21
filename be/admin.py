from django.contrib import admin

from be.models import ChannelImage


@admin.register(ChannelImage)
class PointInstanceAdmin(admin.ModelAdmin):
    list_display = ('file',)
