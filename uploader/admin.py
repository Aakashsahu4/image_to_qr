"""External Imports"""
from django.contrib import admin

"""Internal Imports"""
from . import models


@admin.register(models.UploadedImageModel)
class SubjectAdmin(admin.ModelAdmin):
	list_display = ['id','image','created','modified']