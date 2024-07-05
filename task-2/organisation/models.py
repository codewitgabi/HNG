import uuid
from django.db import models


class Organisation(models.Model):
    orgId = models.UUIDField(primary_key=True, editable=True, default=uuid.uuid4)
    name = models.CharField(max_length=550)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
