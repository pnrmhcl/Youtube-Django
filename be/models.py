from django.db import models


class ChannelImage(models.Model):
    file = models.FileField(upload_to="static")
    channel_id = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.channel_id)
