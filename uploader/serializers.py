"""External Imports"""
from rest_framework import serializers

"""Internal Imports"""
from .models import UploadedImageModel, OwnUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnUser
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImageModel
        fields = ['image','image_type','qr_code_url']