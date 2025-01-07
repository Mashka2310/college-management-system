from django.db import models
from django.contrib.auth import get_user_model
user=get_user_model() 
# auth_table

# Create your models here.


class CourseModel(models.Model):
    course_name=models.CharField(max_length=300)
    course_fee=models.IntegerField()


class StudentModel(models.Model):
    course = models.ForeignKey(CourseModel, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=300)
    stuent_age = models.IntegerField()
    student_address = models.CharField(max_length=300)
    stuent_phone = models.CharField(max_length=10, null=True)
    student_email = models.CharField(max_length=300)
    Image = models.ImageField(upload_to="image/")


class TeacherModel(models.Model):
    # auth_user
    teacher=models.ForeignKey(user,on_delete=models.CASCADE)
    course=models.ForeignKey(CourseModel,on_delete=models.CASCADE)

    teacher_gender=models.CharField(max_length=300)
    teacher_address=models.CharField(max_length=300)
    teacher_phone=models.CharField(max_length=10,null=True)
    teacher_age=models.IntegerField()
    Image=models.ImageField(upload_to="image/")


# auth_user_table + TeacherModel (auth table + connecting table) topic:

