from django.shortcuts import render,redirect
from myapp.models import CourseModel,TeacherModel,StudentModel
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.


def Home_page(request):
    return render(request,"home_page.html")

def Register_page(request):
    course=CourseModel.objects.all()
    return render(request,"signup_page.html",{'course':course})

def add_course_page(request):
    return render(request,"add_course.html")

def admin_home(request):
    return render(request,"admin_home.html")

def teacher_home(request):
    return render(request,"teacher_home.html")

def add_course(request):
    if request.method=="POST":
        crs_name=request.POST["course_name"]
        crs_fee=request.POST["course_fee"]

        course=CourseModel(course_name=crs_name,
                           course_fee=crs_fee)
        course.save()
        return render(request,"add_course.html")
    

def login_page(request):
    return render(request,"login.html")


def login(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]

        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            if(user.is_superuser):
                return redirect("admin_home")
            else:
                request.session['uid']=user.id
                return redirect("teacher_home")
        else:
            messages.info(request,"Invalid username and password")
            return redirect("login_page")
    else:
        return redirect("login_page")
    
def logout(request):
    auth.logout(request)
    return redirect("Home_page")

# { auth + connecting table here..}
def create_user(request):
    if request.method=="POST":

        # first we want to collect authuser fields
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        username=request.POST["username"]
        email=request.POST["email"]
        password=request.POST["password"]
        cpassword=request.POST["cpassword"]


        # then we want to collect TeacherModel fields
        address=request.POST["address"]
        age=request.POST["age"]
        phone=request.POST["phone"]
        gender=request.POST["gender"]

        select=request.POST["select"]

        course=CourseModel.objects.get(id=select)

        # dwfault image
        image=request.FILES.get("file")
        if image==None:
            image="image/img.jpeg"

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "This username is already exist, try new")
                return redirect("Register_page")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "This email is already taken, try new!")
                return redirect("Register_page")
            else:

                # auth user
                user = User.objects.create_user(first_name=first_name,
                                                last_name=last_name,
                                                username=username,
                                                email=email,
                                                password=password)
                user.save()
                # connection
                data = User.objects.get(id=user.id)

                teacher_data=TeacherModel(teacher_address=address,
                                          teacher_age=age,
                                          teacher_phone=phone,
                                          teacher_gender=gender,
                                          Image=image,
                                          course=course,
                                          teacher=data)
                teacher_data.save()
                messages.success(request, "Registration successful, Please Login")

                subject = "Registration Completed"
                message = f"Dear {first_name},\nYour account has been successfully created. \nUsername: {username}\nPassword: {password}"
                recipient = email
                send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)

                messages.success(request, 'Registration is successful')
                return redirect("login_page")          
        else:
            messages.info(request, "Password does not match!")
            return redirect("Register_page")
    else:
        return redirect("Register_page")
    

def profile(request):
    if 'uid' in request.session:
        userId = request.session['uid']
        user = TeacherModel.objects.get(teacher=userId)
        return render(request,'teacher_profile.html',{'user':user})
    else:
        return redirect('login_page')
    
def edit_teacher(request,userId):
    user= TeacherModel.objects.get(teacher=userId)
    course=CourseModel.objects.all()
    return render(request,'edit_teacher.html',{'user':user,'course':course})


def update_teacher(request, userId):
    user = User.objects.get(id=userId)
    teacher = TeacherModel.objects.get(teacher=userId)

    if request.method == "POST":
        # auth user
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.username = request.POST["username"]
        user.email = request.POST["email"]

# teachermodel - teacher
        teacher.teacher_age = request.POST["age"]
        teacher.teacher_address = request.POST["address"]
        teacher.teacher_gender = request.POST["gender"]
        teacher.teacher_phone = request.POST["phone"]

        old = teacher.Image
        new = request.FILES.get("file")

        if old != None and new == None:
            teacher.Image = old
        else:
            teacher.Image = new

        select = request.POST["select"]
        course = CourseModel.objects.get(id=select)
        teacher.course = course

        user.save()
        teacher.save()

        return redirect("profile")

    
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

@login_required
def change_password(request):
    if request.method == "POST":
        old_password = request.POST["old_password"]
        new_password = request.POST["new_password"]
        confirm_new_password = request.POST["confirm_new_password"]

        user = request.user

        if not user.check_password(old_password):
            messages.error(request, "Incorrect old password. Please try again.")
            return redirect("change_password")

        if new_password != confirm_new_password:
            messages.error(request, "New passwords do not match. Please try again.")
            return redirect("change_password")
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user) 

        messages.success(request, "Password changed successfully.")
        return redirect("profile")

    return render(request,"change_password.html")


def add_student_page(request):
    courses = CourseModel.objects.all()
    return render(request, "add_student.html", {"courses": courses})


def add_student(request):
    if request.method=="POST":
        sname=request.POST["sname"]
        sage=request.POST["sage"]
        sphone=request.POST["sphone"]
        semail=request.POST["semail"]
        saddress=request.POST["saddress"]

        select=request.POST["select"]
        course=CourseModel.objects.get(id=select)

        image=request.FILES.get("file")

        if image==None:
            image="image/img.jpeg"

        data=StudentModel(student_name=sname,
                          stuent_age=sage,
                          student_address=saddress,
                          stuent_phone=sphone,
                          course=course,
                          Image=image,
                          student_email=semail)
        data.save()
        messages.success(request,"Successfully created student details!")
        return redirect("admin_home")



def teachers_details(request):
    user=TeacherModel.objects.all()
    return render(request,"teachers_list.html",{"user":user})

def Delete_teacher(request,userId):
    user=User.objects.get(id=userId)
    user.delete()
    return redirect("teachers_details")

def Display_student_details(request):
    student=StudentModel.objects.all()
    return render(request,"student_details.html",{"student":student})

def Edit_student_page(request,pk):
    student=StudentModel.objects.get(id=pk)
    course=CourseModel.objects.all()
    return render(request,"edit_student.html",{'student':student,"course":course})


def Edit_student_details(request,pk):
    if request.method == "POST":
        student = StudentModel.objects.get(id=pk)
        student.student_name = request.POST["sname"]
        student.stuent_age = request.POST["sage"]
        student.stuent_phone = request.POST["sphone"]
        student.student_address = request.POST["saddress"]
        student.student_email = request.POST["semail"]

        new=request.FILES.get("file")
        old=student.Image

        if old!= None and new==None:
            student.Image=old
        else:
            student.Image=new

        select = request.POST["select"]
        course = CourseModel.objects.get(id=select)
        student.course = course
        student.save()
        messages.success(request,"Updated Student details!")
        return redirect("Display_student_details")
    
def Show_all_course(request):
    course=CourseModel.objects.all()
    return render(request,"course_page.html",{'course':course})

def Edit_course(request,pk):
    course=CourseModel.objects.get(id=pk)
    return render(request,"edit_course.html",{'course':course})

def Edit_course_function(request,pk):
    course=CourseModel.objects.get(id=pk)
    if request.method=="POST":
        course.course_name=request.POST.get("cname")
        course.course_fee=request.POST.get("cfee")
        course.save()
        messages.success(request,"Course updated successfully")
        return redirect("Show_all_course")
    

def Delete_course(request,pk):
    delete=CourseModel.objects.get(id=pk)
    delete.delete()
    messages.success(request,"Course deleted successfully")
    return redirect("Show_all_course")





# image project
# authentification -auth user
# athuser table for admin and normal user
# foeignkey (1.add course , 2.add student,3. course details, 4. student datails)
# mail project
# update(edit) and delete(remove)

# auth table + connected table




        



