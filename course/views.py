from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
from .models import Course, CoursePrerequisite

# print(Course.searchByName(Course, 'Algorithms'))
#print(Course.searchByWords(Course, 'Robot'))
#print(Course.searchByCredits(Course, 0)[0])
#print(Course.searchByCode(Course, 'CSDS', 310))
# courses = CoursePrerequisite.searchPrerequisite(CoursePrerequisite, 'Advanced Algorithms')
# for course in courses:
#     print(course.name)

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
    results = None
    if(request.method=='POST'):
        #Do stuff here.
        print(request.POST)
        results = Course.searchByWords(Course, request.POST['course_name'])
        print(results)
    else:
        #New form
        True
    
    return render(request, "search/class-search.html", {'results': results})

def dep_viewer(request):
    return render(request, "search/dep-viewer.html", {})

def course_suggestion(request):
    return render(request, "search/course-suggestion.html", {})