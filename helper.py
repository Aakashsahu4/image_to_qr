"""External Imports"""
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

"""Internal Imports"""
import keys

class CustomResponses():
	"""Custom responses"""

	@staticmethod
	def success_reponse(message,data):
		response_data={
			keys.SUCCESS:True,
			keys.MESSAGE : message,
			keys.DATA :data,
				}
		return response_data

	@staticmethod
	def failure_reponse(message,data):
		response_data={
			keys.SUCCESS:False,
			keys.MESSAGE : message,
			keys.DATA :data,
				}
		return response_data

	@staticmethod
	def serializer_error_message_function(errors):
		"""
		return error message when serializer is not valid
		:param errors: error object
		:returns: string
		"""
		for key, values in errors.items():
			error = [value[:] for value in values]
			err = ' '.join(map(str,error))
			return err
	
	@staticmethod
	def pagination_response(paginator,page,page_count,data):
		Response={
			keys.SUCCESS:True,
			keys.DATA: data,
			keys.PAGE_NUMBER: int(page),
			keys.TOTAL_PAGE: paginator.num_pages,
			keys.PAGE_COUNT: int(page_count),
			keys.TOTAL_COUNT: paginator.count,
		}
		return Response


def validate_image(image):
    allowed_extensions = ['jpg', 'jpeg', 'png']
    validator = FileExtensionValidator(allowed_extensions)
    try:
        validator(image)
        width, height = get_image_dimensions(image)
        if width > 5000 or height > 5000:
            raise ValidationError("Image dimensions should not exceed 5000x5000 pixels.")
    except ValidationError as e:
        return str(e)
    return None