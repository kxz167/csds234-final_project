import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from course.models import Course, CoursePrerequisite

#print(Course.searchByName(Course, 'Algorithms'))
#print(Course.searchByWords(Course, 'Robot'))
#print(Course.searchByCredits(Course, 0)[0])
#print(Course.searchByCode(Course, 'CSDS', 310))

# executer = Course.QueryExecuter()
# result = executer.searchByDeparment('CSDS').searchByCredits(3).resultList()
# for course in result:
#     print(course.name)

# adjacency = CoursePrerequisite.searchPrerequisiteGraph(CoursePrerequisite, 'Advanced Algorithms')
# for course, preqs in adjacency.items():
#     print('Course: ',course.name)
#     for preq in preqs:
#         print(preq.name)

# level200Courses = Course.QueryExecuter().searchByCodeRange(200, 299).resultList()
# for course in level200Courses:
#     print(course.code, ' ', course.name)
    
# credit34Courses = Course.QueryExecuter().searchByCreditRange(3, 5).resultList()
# for course in credit34Courses:
#     print(course.code, ' ', course.name)

# courses = Course.QueryExecuter().searchCoursesAbleToTake(['Modern Robot Programming'])
# for course in courses:
#     print(course.name)

courses = Course.QueryExecuter().suggestedCourse(['Introduction to Programming in Java'], 'CSBS')
for course in courses:
    print(course.name)