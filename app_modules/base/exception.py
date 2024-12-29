import logging
from rest_framework.views import exception_handler
from django.http import JsonResponse
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

def get_response(message="", result={}, status=False, status_code=200):
    return {
        "message": message,
        "result": result,
        "status": status,
        "status_code": status_code,
    }

def get_error_message(error_dict):
    if isinstance(error_dict, dict):
        # Extracting field-specific error messages
        errors = {}
        for field, messages in error_dict.items():
            errors[field] = [str(msg) for msg in messages]
        return errors
    elif isinstance(error_dict, list):
        # If it's a list, return the first error's detail
        return [str(error.get("detail", "An unknown error occurred")) for error in error_dict]
    return "An unknown error occurred"

def handle_exception(exc, context):
    logger.error(f"Exception occurred: {exc}", exc_info=True)

    error_response = exception_handler(exc, context)

    if error_response is not None:
        error = error_response.data
        
        if isinstance(error, dict) and 'detail' in error:
            message = get_error_message(error)
            error_response.data = get_response(
                message=message,
                status_code=error_response.status_code,
                status=False
            )
        elif isinstance(error, list):
            message = get_error_message(error)
            error_response.data = get_response(
                message=message,
                status_code=error_response.status_code,
                status=False
            )

    return error_response

class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 500:
            response_data = get_response(
                message="Internal server error, please try again later",
                status_code=response.status_code
            )
            return JsonResponse(response_data, status=response_data["status_code"])

        if response.status_code == 404:
            response_data = get_response(
                message="Page not found, invalid URL",
                status_code=response.status_code
            )
            return JsonResponse(response_data, status=response_data["status_code"])

        return response