from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return(self.first_name + " " +self.last_name)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return(self.user.first_name + " " + self.user.last_name)
    

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return(self.user.first_name + " " + self.user.last_name)
    
class Course(models.Model):
    name = models.CharField(max_length=255)
    instructor = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student,blank=True, null = True)
    capacity = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    SUN = 0
    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    FRI = 5
    SAT = 6

    DAYS_OF_WEEK_CHOICES = (
        (SUN, 'Sunday'),
        (MON, 'Monday'),
        (TUE, 'Tuesday'),
        (WED, 'Wednesday'),
        (THU, 'Thursday'),
        (FRI, 'Friday'),
        (SAT, 'Saturday'),
    )

    # loads choices from defined list
    eligible_days = models.CharField(max_length=14,choices=DAYS_OF_WEEK_CHOICES,
        blank=False)

    def __str__(self):
        return(self.name)

class Chat(models.Model):
    course= models.ForeignKey(Course)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    message = models.TextField()

    def __unicode__(self):
        return self.message