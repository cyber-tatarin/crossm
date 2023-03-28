from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
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
            return HttpResponseRedirect(f"{reverse_lazy('login')}?next={reverse_lazy('user-enrollment')}")


class AccessForMembersOnlyMixin:
    redirect_manager = {User.NEWBIE: AccessForCompletesOnlyMixin.redirect_to_set_profile_info,
                        User.COMPLETE: AccessForCompletesOnlyMixin.redirect_to_enrollment,
                        }
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role < User.INVITED:
                redirect_func = self.redirect_manager[request.user.role]
                return redirect_func()
            else:
                return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(f"{reverse_lazy('login')}?next={reverse_lazy('user-enrollment')}")
        

class AccessForCompleteNonMembersOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role >= User.INVITED:
                return redirect('offers:catalog')
            elif request.user.role < User.COMPLETE:
                return redirect('set-profile-info')
            else:
                return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(f"{reverse_lazy('login')}?next={reverse_lazy('user-enrollment')}")
        