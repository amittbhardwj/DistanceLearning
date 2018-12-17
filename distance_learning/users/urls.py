from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home,name='home'),
    url(r'^student/dashboard$', views.StudentDashBoard.as_view(),name='student_dashboard'),
    url(r'^teacher/dashboard$', views.TeacherDashBoard.as_view(),name='teacher_dashboard'),
     url(r'^teacher/createcourse$', views.CourseCreate.as_view(),name='create_course'),
]