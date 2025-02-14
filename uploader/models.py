"""External Imports"""
from django.db import models
from django.contrib.auth.models import AbstractUser


class OwnUser(AbstractUser):
	"""Model to Store Teachers Data"""

	password = models.CharField(max_length=10)

	def __str__(self):
		return self.username
	


class UploadedImageModel(models.Model):

	class ImageType(models.Choices):
			'portrait' == 'Portrait'
			'landscape' == 'Landscape'

	user = models.ForeignKey(OwnUser, on_delete=models.CASCADE,related_name='ownuser')
	image = models.ImageField(upload_to='images/')
	image_type = models.CharField(max_length=10, choices=ImageType.choices,default='portrait')
	qr_code_url = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

	created = models.DateTimeField(auto_now=False, auto_now_add=True)
	modified = models.DateTimeField(auto_now=True, auto_now_add=False)
