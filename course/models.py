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
    
    class QueryExecuter:
        def __init__(self):
            self.result = Course.courses.all()
        
        #returns a list of courses by name
        def searchByName(self, name):
            self.result = self.result.filter(name__iexact=name)
            return self
        
        #returns a list of courses containing input words
        def searchByWords(self, words):
            self.result = self.result.filter(name__icontains=words)
            return self
        
        #returns a list of courses by their credits
        def searchByCredits(self, credit):
            self.result = self.result.filter(credits__contains=NumericRange(credit, credit + 1))
            return self
        
        #searches a course by its code
        def searchByCode(self, code):
            self.result = self.result.filter(code=code)
            return self
        
        #searches a course by its department
        def searchByDepartment(self, department):
            self.result = self.result.filter(department__abbreviation__iexact=department)
            return self
        
        #return a course by its id
        def searchByID(self, cid):
            self.result = self.result.filter(id = cid)[0]
            return self
        
        #returns a course by its code and department
        def searchByDeparment(self, department):
            self.result = self.result.filter(department__abbreviation__iexact=department)
            return self
        
        #search by range of credits
        def searchByCreditRange(self, leftBound, rightBound):
            self.result = self.result.filter(credits__overlap=[leftBound, rightBound])
            return self
        
        #search by range of codes
        def searchByCodeRange(self, leftBound, rightBound):
            self.result = self.result.filter(code__range=[leftBound, rightBound])
            return self

        #returns list of courses given their name
        def coursesGivenNames(self, names):
            courses = list()
            for name in names:
                courses.append(Course.courses.filter(name__iexact=name))
            return courses
        
        #searches courses able to take
        def searchCoursesAbleToTake(self, takenCoursesNames, includeTakenCourse):
            temp = list(self.result)
            courses = list()
            for course in temp:
                prerequisites = list(CoursePrerequisite.prerequisite.filter(course_id=course.id))
                haveAllPreq = True
                for preq in prerequisites:
                    if (Course.searchByID(Course, preq.prerequisite_id) != None): 
                        if not (Course.searchByID(Course, preq.prerequisite_id).name in takenCoursesNames):
                            haveAllPreq = False
                if (haveAllPreq):
                    courses.append(course)
            return courses if includeTakenCourse else self.CoursesNotTaken(courses, takenCoursesNames)
        
        #minus taken courses from returning courses
        def CoursesNotTaken(self, courses, takenCoursesName):
            result = list()
            for course in courses:
                if not (course.name in takenCoursesName):
                    result.append(course)
            return result
        #transforms names of courses into ID
        def Names2IDs(self, takenCoursesName):
            IDs = list()
            for name in takenCoursesName:
                IDs.append(Course.searchByName(Course, name)[0].id)
            return IDs
        
        #returns list of ids of suggested courses
        def suggestedCourses(self, program):
            suggestedPlan = list()
            if (program == 'CSBS'):
                plan = CsbsSuggestedPlan.objects.all()
                for plannedCourse in plan:
                    suggestedPlan.append(plannedCourse.course.id)
            if (program == 'CSBA'):
                plan = CsbaSuggestedPlan.objects.all()
                for plannedCourse in plan:
                    suggestedPlan.append(plannedCourse.course.id)
            if (program == 'DSBS'):
                plan = DsbsSuggestedPlan.objects.all()
                for plannedCourse in plan:
                    suggestedPlan.append(plannedCourse.course.id)        
            return suggestedPlan
        
        #transforms taken courses to taken planned courses
        def takenCourses2Planned(self, takenCoursesID):
            result = list()
            for courseID in takenCoursesID:
                tempID = courseID
                if (CsBreadth.objects.filter(course__id = tempID)):
                    tempID = 111
                elif (CsDepth.objects.filter(course__id = tempID)):
                    tempID = 110
                elif (CsTechnical.objects.filter(course__id = tempID)):
                    tempID = 109
                result.append(tempID)
            return result
        
        #add elective course to input list
        def addElective(self, id, result, takenIDs):
            if (id == 111):
                breadthCourses = CsBreadth.objects.all()
                for breath in breadthCourses:
                    if not (breath.course.id in takenIDs):
                        result.append(breath.course.id)
                        return
            elif (id == 110):
                depthCourses = CsDepth.objects.all()
                for depth in depthCourses:
                    if not (depth.course.id in takenIDs):
                        result.append(depth.course.id)
                        return
            elif (id == 109):
                technicalCourses = CsTechnical.objects.all()
                for tech in technicalCourses:
                    if not (tech.course.id in takenIDs):
                        result.append(tech.course.id)
                        return
        
        #return a list of suggested course
        def suggestedCourse(self, takenCoursesName, program):
            result = list()
            takenCoursesID = self.Names2IDs(takenCoursesName)
            suggestedPlan = self.suggestedCourses(program)
            takenPlannedCourses = self.takenCourses2Planned(takenCoursesID)
            print(takenPlannedCourses[0])
            i = 0
            for suggestID in suggestedPlan:
                if (suggestID in takenPlannedCourses):
                    takenPlannedCourses.remove(suggestID)
                else:
                    i += 1
                    if (109 <= suggestID and suggestID <= 111):
                        self.addElective(suggestID, result, takenCoursesID)
                    else:
                        result.append(suggestID)
                if (i >= 5):
                    break
            courses = list()
            for ID in result:
                courses.append(Course.searchByID(Course, ID))
            return courses
        
        # returns the list of result of this query
        def resultList(self):
            temp = list(self.result)
            courses = list()
            for course in temp:
                if (course.code != None):
                    courses.append(course)
            return courses
    
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
        return Course.courses.filter(id = cid)[0] if len(Course.courses.filter(id = cid)) > 0 else None
    
    #returns a list of courses by name
    def searchByName(self, name):
        return list(Course.courses.filter(name__iexact=name))

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
    
    #return an adjacency list for prerequisite of input course
    def searchPrerequisiteGraph(self, name):
        result = {}
        preqs = self.searchPrerequisite(name)
        course = Course.searchByName(Course, name)
        courses = list()
        prerequisites = list(CoursePrerequisite.prerequisite.filter(course_id=course[0].id))
        for preq in prerequisites:
            courses.append(Course.searchByID(Course, preq.prerequisite_id))
        result[course[0]] = courses
        for preq in preqs:
            if not (preq in result):
                courses = list()
                prerequisites = list(CoursePrerequisite.prerequisite.filter(course_id=preq.id))
                for pre in prerequisites:
                    courses.append(Course.searchByID(Course, pre.prerequisite_id))
                result[preq] = courses
        return result

    #return an adjacency list for prerequisite of input course
    def searchPrerequisiteGraphDisplay(self, name):
        result = {}
        preqs = self.searchPrerequisite(name)
        course = Course.searchByName(Course, name)
        courses = list()
        prerequisites = list(CoursePrerequisite.prerequisite.filter(course_id=course[0].id))
        for preq in prerequisites:
            courses.append(Course.searchByID(Course, preq.prerequisite_id).name)
        result[course[0].name] = courses
        for preq in preqs:
            if not (preq in result):
                courses = list()
                prerequisites = list(CoursePrerequisite.prerequisite.filter(course_id=preq.id))
                for pre in prerequisites:
                    courses.append(Course.searchByID(Course, pre.prerequisite_id).name)
                result[preq.name] = courses
        return result
    
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

class DsbsSuggestedPlan(models.Model):
    id = models.IntegerField(primary_key=True)
    course = models.ForeignKey(Course, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dsbs_suggested_plan'

class CsbsSuggestedPlan(models.Model):
    id = models.IntegerField(primary_key=True)
    course = models.ForeignKey(Course, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'csbs_suggested_plan'

class CsbaSuggestedPlan(models.Model):
    id = models.IntegerField(primary_key=True)
    course = models.ForeignKey(Course, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'csba_suggested_plan'

class CsTechnical(models.Model):
    course = models.ForeignKey('Course', models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'cs_technical'

class CsDepth(models.Model):
    course = models.ForeignKey('Course', models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'cs_depth'

class CsBreadth(models.Model):
    course = models.ForeignKey('Course', models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'cs_breadth'


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