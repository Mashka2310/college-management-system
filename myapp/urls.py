from . import views
from django.urls import path


urlpatterns= [
    path("",views.Home_page,name="Home_page"),
    path("Register_page",views.Register_page,name="Register_page"),
    path("login_page",views.login_page,name="login_page"),
    path("admin_home",views.admin_home,name="admin_home"),
    path("teacher_home",views.teacher_home,name="teacher_home"),
    
    path("add_course_page",views.add_course_page,name="add_course_page"),
    path("add_course",views.add_course,name="add_course"),
    path("login_page",views.login_page,name="login_page"),
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),

    path("create_user",views.create_user,name="create_user"),
    path("profile",views.profile,name="profile"),
    path("edit_teacher/<int:userId>",views.edit_teacher,name="edit_teacher"),
    path("update_teacher/<int:userId>",views.update_teacher,name="update_teacher"),
    path("change_password",views.change_password,name="change_password"),
    path("add_student_page",views.add_student_page,name="add_student_page"),
    path("add_student",views.add_student,name="add_student"),

    path("teachers_details",views.teachers_details,name="teachers_details"),
    path("Delete_teacher/<int:userId>",views.Delete_teacher,name="Delete_teacher"),
    path("Display_student_details",views.Display_student_details,name="Display_student_details"),
    path("Edit_student_page/<int:pk>",views.Edit_student_page,name="Edit_student_page"),
    path("Edit_student_details/<int:pk>",views.Edit_student_details,name="Edit_student_details"),
    path("Show_all_course",views.Show_all_course,name="Show_all_course"),
    
    path("Edit_course/<int:pk>",views.Edit_course,name="Edit_course"),
    path("Edit_course_function/<int:pk>",views.Edit_course_function,name="Edit_course_function"),
    path("Delete_course/<int:pk>",views.Delete_course,name="Delete_course"),
]