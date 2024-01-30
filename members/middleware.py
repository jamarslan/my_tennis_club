import datetime
import logging
import sys

from django.http import HttpResponseForbidden
from django.http import HttpResponseServerError
from django.views.debug import technical_500_response


class TimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before the view is called
        print(f"Request received at {datetime.datetime.now()}")
        response = self.get_response(request)
        # Code to be executed for each response after the view is called
        return response


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log information about the request
        logging.info(f"Request received: {request.path}")

        response = self.get_response(request)

        # Log information about the response
        logging.info(f"Response status code: {response.status_code}")

        return response


class IPBlockingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check the request's IP address and block if necessary
        blocked_ips = ['127.0.0.1']  # Add your blocked IPs
        if request.META['REMOTE_ADDR'] in blocked_ips:
            return HttpResponseForbidden("Access Forbidden")

        response = self.get_response(request)
        return response


class ExceptionPageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            if request.META.get('HTTP_ACCEPT', 'text/html') == 'application/json':
                # Return a JSON response for AJAX requests
                return HttpResponseServerError(content_type='application/json')
            else:
                # Render the default Django technical 500 response
                return technical_500_response(request, *sys.exc_info())

        return response
