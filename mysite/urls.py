from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import course.views as vm

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", vm.index, name="index"),
    path("db/", vm.db, name="db"),
    path("sample", vm.sample, name="sample"),
    path("class-search", vm.class_search, name="class_search"),
    path("course-deps", vm.course_deps, name="course_deps"),
    path("avail-course", vm.avail_course, name="avail_course"),
    path("course-suggestion", vm.course_suggestion, name="course_suggestion"),
    # path("admin/", admin.site.urls),
]
