from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
from .models import Course, CoursePrerequisite

# Defines a simple filter that takes in arguments and whittles down the query.
def simple_filter(query, args):
    if( args['credit_min']):
        if( args['credit_max']):
            query.searchByCreditRange(int(args['credit_min']), int(args['credit_max']))
        else:                
            query.searchByCredits(int(args['credit_min']))

    if( args['code_min']):
        if( args['code_max']):
            query.searchByCodeRange(int(args['code_min']), int(args['code_max']))
        else:                
            query.searchByCode(int(args['code_min']))

    if( args['department']):
        query.searchByDepartment(args['department'])

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

        # Create simple query:
        query = Course.QueryExecuter()
        simple_filter(query, args)
        if( args['course_name']):
            query.searchByWords(args['course_name'].strip())
    else:
        query = Course.QueryExecuter()
        args = {}
    
    results = query.resultList()
    return render(request, "search/class-search.html", {'prev_query': args, 'results': results})

def course_deps(request):
    results = None
    args = None
    adjacency = None

    if(request.method=='POST'):
        args = request.POST

        results = CoursePrerequisite().searchPrerequisite(args['course_name'])
        adjacency = CoursePrerequisite().searchPrerequisiteGraphDisplay(args['course_name'])

    return render(request, "search/course-deps.html", {'prev_query': args, 'results': results, 'graph_results': adjacency})

def avail_course(request):
    results = None
    args = None
    if(request.method=='POST'):
        args = request.POST

        # Create basic query:
        query = Course.QueryExecuter()
        simple_filter(query, args)

        # Course list: 
        course_string = args['courses']
        courses = [course.strip() for course in course_string.split(",") if course.strip()]

        # Uncomment when implemented
        # result = query.availableCourses(courses)

    print(results)
    return render(request, "search/avail-course.html", {'prev_query': args, 'results': results})

def course_suggestion(request):
    results = None
    args = None
    if(request.method=='POST'):
        args = request.POST

        query = Course.QueryExecuter()

        # program:
        program = args['program']

        # Course list: 
        course_string = args['courses']
        courses = [course.strip() for course in course_string.split(",") if course.strip()]

        print(courses)
        print(program)
        # Uncomment when implemented
        # result = query.suggestedCourse(program, courses)

    return render(request, "search/course-suggestion.html", {'prev_query':args, 'results':results})

def sample(request):
    return render(request, "search/sample.html", {})