from django.db import models, transaction
from django.utils import crypto, timezone
from guardian.shortcuts import (assign_perm, get_objects_for_user,
                                get_perms_for_model, get_user_perms,
                                get_users_with_perms, remove_perm)


class ControlService(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True, help_text="The name of this endpoint/host Control Service .")
    api_user = models.CharField(max_length=255, null=True, blank=True, help_text="The user/login identify for accessing Control Service's API.")
    api_pw = models.CharField(max_length=255, null=True, blank=True, help_text="The user/login password or API KEY for accessing Control Service's API.")
    api_root_path = models.CharField(max_length=255, null=True, blank=True, help_text="The domain and initial path for accessing Control Service's API.")
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        # For the admin, notification strings
        return self.name
