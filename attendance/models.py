from django.db import models
from django.conf import settings
from django.utils import timezone

class Personnel(models.Model):
    rank = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    is_commander = models.BooleanField(default=False)
    platoon = models.IntegerField()
    company = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default = 1,
        related_name='personnel_created_by',
        db_column='created_by'
        )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default = 1,
        related_name='personnel_updated_by',
        db_column='updated_by'
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return self.name

class Parade(models.Model):
    date = models.DateField()
    time_of_day = models.IntegerField()
    time = models.TimeField(default=timezone.now)
    total_strength = models.IntegerField(null=True, blank=True)
    current_strength = models.IntegerField(null=True, blank=True)
    commander_strength = models.IntegerField(null=True, blank=True)
    personnel_strength = models.IntegerField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default = 1,
        related_name='parade_created_by',
        db_column='created_by'
        )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default = 1,
        related_name='parade_updated_by',
        db_column='updated_by'
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


class Absence(models.Model):
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    parade = models.ForeignKey(Parade, on_delete=models.CASCADE)
    is_MC = models.BooleanField(default=False)
    is_MA = models.BooleanField(default=False)
    is_off = models.BooleanField(default=False)
    is_leave = models.BooleanField(default=False)
    is_other = models.BooleanField(default=False)
    remarks = models.TextField(default=None)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default = 1,
        related_name='absence_created_by',
        db_column='created_by'
        )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default = 1,
        related_name='absence_updated_by',
        db_column='updated_by'
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


class Status(models.Model):
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    parade = models.ForeignKey(Parade, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    remarks = models.TextField(default=None)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default = 1,
        related_name='status_created_by',
        db_column='created_by'
        )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default = 1,
        related_name='status_updated_by',
        db_column='updated_by'
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
