from django.utils.deprecation import MiddlewareMixin
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.utils.functional import cached_property


class StateMiddleware(MiddlewareMixin):

    @classmethod
    def get_model_class(cls):
        from django.contrib.sessions.models import Session
        return Session

    @cached_property
    def model(self):
        return self.get_model_class()

    def session_is_expire(self, session_key):
        try:
            session = self.model.objects.get(
                session_key=session_key
            )

            if session.expire_date < timezone.now():
                return True
        except self.model.DoesNotExist as e:
            return False
            
    def process_request(self, request):
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)

        if self.session_is_expire(session_key):
            messages.error(request, "Your session expired after a long inactivity!")
