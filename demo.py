import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from hello.models import Course, CoursePrerequisite

#print(Course.searchByName(Course, 'Algorithms'))
#print(Course.searchByWords(Course, 'Robot'))
#print(Course.searchByCredits(Course, 0)[0])
#print(Course.searchByCode(Course, 'CSDS', 310))
courses = CoursePrerequisite.searchPrerequisite(CoursePrerequisite, 'Advanced Algorithms')
for course in courses:
    print(course.name)