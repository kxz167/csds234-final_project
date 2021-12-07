from django.db import models
from django.contrib.postgres.fields import IntegerRangeField
from psycopg2.extras import NumericRange

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Course(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.IntegerField(blank=True, null=True)
    department = models.ForeignKey('Department', models.DO_NOTHING, blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    credits = IntegerRangeField(blank=True, null=True)  # This field type is a guess.
    description = models.TextField(blank=True, null=True)
    standing_prequisite = models.TextField(blank=True, null=True)
    standing_recommendation = models.TextField(blank=True, null=True)
    courses = models.Manager()
    
    #returns a list of courses by name
    def searchByName(self, name):
        return list(Course.courses.filter(name__iexact=name))
    
    #returns a list of courses containing input words
    def searchByWords(self, words):
        return list(Course.courses.filter(name__icontains=words))
    
    #returns a list of courses by their credits
    def searchByCredits(self, credit):
        return list(Course.courses.filter(credits__contains=NumericRange(credit, credit + 1)))
    
    #returns a course by its code and department
    def searchByCode(self, department, code):
        return list(Course.courses.filter(code=code).filter(department__abbreviation__iexact=department))
    #return a course by its id
    def searchByID(self, cid):
        return Course.courses.filter(id = cid)[0]
    class Meta:
        managed = False
        db_table = 'course'


class CoursePrerequisite(models.Model):
    course_id = models.IntegerField(primary_key=True)
    prerequisite_id = models.IntegerField()
    #course_id = models.ForeignKey('Course', models.DO_NOTHING, related_name='cid')
    #prerequisite_id = models.ForeignKey('Course', models.DO_NOTHING, related_name='preq')
    #prerequisite_id = models.IntegerField()
    prerequisite = models.Manager()
    
    #returns all prerequisites of input course
    def searchPrerequisite(self, name):
        course = Course.searchByName(Course, name)
        prerequisites = list(CoursePrerequisite.prerequisite.filter(course_id=course[0].id))
        courses = list()
        for preq in prerequisites:
            courses.append(Course.searchByID(Course, preq.prerequisite_id))
        for course in courses:
            prerequisites = list(CoursePrerequisite.prerequisite.filter(course_id=course.id))
            for preq in prerequisites:
                if not (Course.searchByID(Course, preq.prerequisite_id) in courses):
                    courses.append(Course.searchByID(Course, preq.prerequisite_id))
        return courses
    
    class Meta:
        managed = False
        db_table = 'course_prerequisite'
        unique_together = (('course_id', 'prerequisite_id'))


class CourseRecommendation(models.Model):
    course_id = models.IntegerField(primary_key=True)
    recommendation_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'course_recommendation'
        unique_together = (('course_id', 'recommendation_id'),)


class Department(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    abbreviation = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'department'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Greeting(models.Model):
    when = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'hello_greeting'