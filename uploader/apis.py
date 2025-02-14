"""External Imports"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.response import Response
import qrcode, io
# from django.contrib.auth.models import User

"""Internal Imports"""
from . import models
from . import serializers
import keys
import messages
from helper import CustomResponses, validate_image


class SignupAPI(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username and password:
            if models.OwnUser.objects.filter(username=username).exists():
                return Response(
                    CustomResponses.failure_reponse(messages.USER_EXISTS, []),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = serializers.UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    CustomResponses.success_reponse(messages.USER_CREATED, serializer.data),
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                CustomResponses.serializer_error_message_function(serializer.errors),
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            CustomResponses.failure_reponse(messages.DATA_REQUIRED, []),
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginAPI(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(CustomResponses.failure_reponse(messages.DATA_REQUIRED, []),
                            status=status.HTTP_400_BAD_REQUEST)

        user_instance = models.OwnUser.objects.filter(username=username).first()

        if user_instance and user_instance.password == password:  # Directly checking password
            refresh = RefreshToken.for_user(user_instance)
            return Response({
                keys.ACCESS_TOKEN: str(refresh.access_token),
                keys.REFRESH_TOKEN: str(refresh),
            }, status=status.HTTP_200_OK)

        return Response(CustomResponses.failure_reponse(messages.INVALID_CREDENTIALS, []),
                        status=status.HTTP_400_BAD_REQUEST)


from django.core.files.base import ContentFile
class UploadImageAPI(APIView):
    permission_classes = [IsAuthenticated]  # Enforce authentication
    
    def post(self, request):
        user = request.user  # Get authenticated user

        if 'image' not in request.data or 'image_type' not in request.data:
            return Response({'error': "Image and image_type are required."}, status=status.HTTP_400_BAD_REQUEST)

        image = request.data.get('image')
        image_type = request.data.get('image_type')

        # Validate image format
        validation_error = validate_image(image)
        if validation_error:
            return Response({'error': validation_error}, status=status.HTTP_400_BAD_REQUEST)

        # Create image instance with the authenticated user
        image_instance = models.UploadedImageModel.objects.create(
            user=user,
            image=image,
            image_type=image_type
        )

        # Generate QR code for the image
        qr_url = request.build_absolute_uri(image_instance.image.url)
        qr = qrcode.make(qr_url)
        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")

        # Save QR code image
        image_instance.qr_code_url.save(f"qr_{image_instance.id}.png", ContentFile(buffer.getvalue()), save=True)

        return Response({'message': "Successfully added", "image_id": image_instance.id}, status=status.HTTP_201_CREATED)


class GalleryAPI(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    def get(self, request):
        # Get images only for the logged-in user
        user_images = models.UploadedImageModel.objects.filter(user=request.user).order_by('-created')

        if not user_images.exists():
            return Response({"message": "No images found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UploadedImageSerializer(user_images, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

