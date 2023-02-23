from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import TemplateView
from django_ratelimit.exceptions import Ratelimited
from users.views import get_profile_ph


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


def handler403(request, exception=None):
    if isinstance(exception, Ratelimited):
        return JsonResponse({'text': 'banned', 'message': 'Вы превысили допустимый лимит запросов'})
    return HttpResponseForbidden('Forbidden')


class InstructionView(TemplateView):
    template_name = 'instruction.html'

    def get_context_data(self, **kwargs):
        return {'profile_ph': get_profile_ph(self.request)}
