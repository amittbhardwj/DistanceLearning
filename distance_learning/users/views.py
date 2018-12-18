from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DetailView

#from ..decorators import student_required
from .forms import  StudentSignUpForm, TeacherSignUpForm, CourseForm
from .models import Student,Teacher, User, Course, Chat


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
    context_object_name = "course_list"

    def get_queryset(self):
        result = []
        course = Course.objects.all()
        for i in course:
            if self.request.user.student not in i.students.all():
                result.append(i)
        print(result)   
        return result

class EnrolledCourses(ListView):
    model = Course
    template_name = 'enrolled_courses.html'
    context_object_name = "course_list"

    def get_queryset(self):
        result = []
        course = Course.objects.all()
        for i in course:
            print(self.request.user.student,i.students.all())
            if self.request.user.student in i.students.all():
                result.append(i)
        print(result)    
        return result

class TeacherDashBoard(ListView):
    model = Course
    template_name = 'teacher_dashboard.html'

    def get_queryset(self):
        result = Course.objects.filter(instructor=self.request.user.teacher)
        return result


class CourseDetailView(DetailView):
    model = Course
    template_name = 'course_details.html'


def enroll(request,course_id):
    course = Course.objects.get(id=course_id)
    course.students.add(request.user.student)
    course.save()

    return render(request,'enroll_sucess.html')


def Post(request,course_id):
    if request.method == "POST":
        print(request.POST)
        msg = request.POST.get('chat-msg', None)
        username = request.user.username
        print(msg)
        c = Chat(user=request.user, message=username +" : "+msg,course=Course.objects.get(id=course_id))

        #if(msg[0:6] == "Robot:"):
        #callRobot(msg, request)
            
        
        #msg = request.user.username+": "+msg

       # c = Chat(user=request.user, message=msg)

        if msg != '':            
            c.save()
        #mg = src="https://scontent-ord1-1.xx.fbcdn.net/hprofile-xaf1/v/t1.0-1/p160x160/11070096_10204126647988048_6580328996672664529_n.jpg?oh=f9b916e359cd7de9871d8d8e0a269e3d&oe=576F6F12"
        return redirect('chathome',course_id=course_id)
    else:
        return HttpResponse('Request must be POST.')

def Messages(request,course_id):
    c = Chat.objects.filter(course=course_id)
    return render(request, 'alpha/messages.html', {'chat': c})

def Home(request,course_id):
    c = Chat.objects.filter(course=course_id)
    return render(request, "alpha/home.html", {'home': 'active', 'chat': c, 'course_id':course_id})

