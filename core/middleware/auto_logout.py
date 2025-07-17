from django.conf import settings
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
import time

class AutoLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        current_time = int(time.time())
        session_timeout = getattr(settings, 'AUTO_LOGOUT_DELAY', 1800)  # 30 minutes default

        last_activity = request.session.get('last_activity', current_time)
        if current_time - last_activity > session_timeout:
            from django.contrib.auth import logout
            logout(request)
            request.session.flush()  # Clear all session data
            request.session['session_expired'] = True  # Set flag
            return redirect('login')

        request.session['last_activity'] = current_time
