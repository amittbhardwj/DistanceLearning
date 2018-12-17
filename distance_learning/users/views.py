from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, TemplateView

#from ..decorators import student_required
from .forms import  StudentSignUpForm, TeacherSignUpForm, CourseForm
from .models import Student,Teacher, User, Course


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class CourseCreate(CreateView):
    model =  Course
    form_class = CourseForm
    template_name = 'course_create.html'

    def form_valid(self,form):
        course = form.save(commit=False)
        course.instructor = self.request.user.teacher
        course.save()
        return redirect('teacher_dashboard')
        

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_student:
           return redirect('student_dashboard')

        if request.user.is_teacher:
            return redirect('teacher_dashboard')
        
        
    return render(request, 'home.html')

class StudentDashBoard(ListView):
    model = Course
    template_name = 'student_dashboard.html'


class TeacherDashBoard(ListView):
    model = Course
    template_name = 'teacher_dashboard.html'

    def get_queryset(self):
        result = Course.objects.filter(instructor=self.request.user.teacher)
        return result

