
from accounts.models import Position, Department, Employee

TRACKED_MODELS = [Position, Department, Employee]

from django.utils.deprecation import MiddlewareMixin
import threading

_thread_locals = threading.local()

class CurrentUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _thread_locals.user = request.user if request.user.is_authenticated else None

    @staticmethod
    def get_current_user():
        return getattr(_thread_locals, 'user', None)