from django.shortcuts import redirect
from .models import User


class AccessForCompletesOnlyMixin:
    @staticmethod
    def redirect_to_set_profile_info():
        return redirect('set-profile-info')
    
    @staticmethod
    def redirect_to_enrollment():
        return redirect('user-enrollment')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role == User.NEWBIE:
                return self.redirect_to_set_profile_info()
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')
            