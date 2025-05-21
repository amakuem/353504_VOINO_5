# myapp/middleware.py
import pytz
from django.utils import timezone

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tz_name = request.session.get('timezone', 'Europe/Minsk')
        try:
            timezone.activate(pytz.timezone(tz_name))
        except pytz.UnknownTimeZoneError:
            timezone.deactivate()
        return self.get_response(request)