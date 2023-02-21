from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render
from django_ratelimit.exceptions import Ratelimited


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


def handler403(request, exception=None):
    if isinstance(exception, Ratelimited):
        return JsonResponse({'text': 'banned', 'message': 'Вы превысили допустимый лимит запросов'})
    return HttpResponseForbidden('Forbidden')
