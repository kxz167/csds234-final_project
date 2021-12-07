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
        args = request.POST

        print(request.POST)
        # print(results)
        query = Course.QueryExecuter()

        if( args['credit_min']):
            if( args['credit_max']):
                query.searchByCreditRange(int(args['credit_min']), int(args['credit_max']))
            else:                
                query.searchByCredits(int(args['credit_min']))

        if( args['code_min']):
            if( args['code_max']):
                # query.searchByCodeRange(int(args['code_min']), int(args['code_max']))
                True
            else:                
                query.searchByCode(int(args['code_min']))

        if( args['department']):
            query.searchByDepartment(args['department'])

        if( args['course_name']):
            query.searchByWords(args['course_name'])

        #Do stuff here.
    else:
        #New form
        query = Course.QueryExecuter()
        args = {}
    
    results = query.resultList()
    print(results)
    return render(request, "search/class-search.html", {'prev_query': args, 'results': results})

def course_deps(request):
    return render(request, "search/dep-viewer.html", {})

def course_suggestion(request):
    return render(request, "search/course-suggestion.html", {})