from django.db import models
from pgcrypto import fields


class EncryptedCRUDTimestampsModelMixin(models.Model):
    """
    `created_at` will be set on creation.
    `modified_at` will be updated on saves.
    Both values will be encrypted.
    """
    created_at = fields.DateTimePGPSymmetricKeyField(auto_now_add=True)
    modified_at = fields.DateTimePGPSymmetricKeyField(auto_now=True)

    class Meta:
        abstract = True
