from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect

from datetime import datetime


def hello_world(request):
    """Return a greeting"""
    now = datetime.now().strftime('%b %dth, %Y - %H:%M hrs')
    return HttpResponse(f'Oh, hi! Current server time is {now}')


def sort_integers(request):
    """Return a JSON response with sorted integers"""
    numbers = request.GET['numbers'].split(',')
    numbers = sorted(list(map(int, numbers)))
    numbers = dict(enumerate(numbers))
    # print(type(numbers))
    # print(numbers)
    return JsonResponse(numbers, json_dumps_params={'indent': 4})


def person(request, name, age):
    """Return a greeting"""
    if age < 12:
        message = f'Sorry {name}, you are not allowed here'
    else:
        message = f'Hello {name}, welcome to Platzigram'
    return HttpResponse(message)


def home(request):
    return redirect("feed")
