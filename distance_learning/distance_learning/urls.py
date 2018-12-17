"""distance_learning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from users import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('accounts/', include('django.contrib.auth.urls')),
    url('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    url('accounts/student/', views.StudentSignUpView.as_view(), name='student_signup'),
    url('accounts/teacher/', views.TeacherSignUpView.as_view(), name='teacher_signup'),
    url('', include('users.urls')),
]
