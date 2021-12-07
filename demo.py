import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from course.models import Course, CoursePrerequisite

#print(Course.searchByName(Course, 'Algorithms'))
#print(Course.searchByWords(Course, 'Robot'))
#print(Course.searchByCredits(Course, 0)[0])
#print(Course.searchByCode(Course, 'CSDS', 310))
executer = Course.QueryExecuter()
result = executer.searchByDeparment('CSDS').searchByCredits(3).resultList()
for course in result:
    print(course.name)