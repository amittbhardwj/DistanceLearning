from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home,name='home'),
    url(r'^student/dashboard$', views.StudentDashBoard.as_view(),name='student_dashboard'),
     url(r'^student/enrolled$', views.EnrolledCourses.as_view(),name='enrolled_courses'),
    url(r'^teacher/dashboard$', views.TeacherDashBoard.as_view(),name='teacher_dashboard'),
    url(r'^teacher/createcourse$', views.CourseCreate.as_view(),name='create_course'),
    url(r'^course/(?P<pk>\d+)$', views.CourseDetailView.as_view(), name='course_detail'),
    url(r'^(?P<course_id>\d+)/enroll/$', views.enroll, name='enroll'),
]