from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})


def class_search(request):
    return render(request, "search/class-search.html", {})

def dep_viewer(request):
    return render(request, "search/dep-viewer.html", {})

def course_suggestion(request):
    return render(request, "search/course-suggestion.html", {})