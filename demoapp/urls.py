from django.urls import path
from . import views

urlpatterns = [
   # path("",views.base,name="base"),
    path("",views.home,name="home"),
    path("login/", views.login),
    path("register/", views.regis),
    path("student/logout/", views.lgout),
    path("mentor/logout/", views.lgout),
    path("student/", views.student),
    path("mentor/", views.mentor),
    # path("pdf/",views.venue_pdf),
    path("studentpdf/",views.student_report),
    path("meetingpdf/",views.meet_report),
    path("thesispdf/",views.thesis_report),
    path("coursepdf/",views.course_report),
    path("adminpdf/",views.admin_report),
    path("centerpdf/",views.center_report),
    path("mentorpdf/",views.mentor_report),
    path("locpdf/",views.location_report),
    path("vivapdf/",views.viva_report),
    path("studentform/",views.add_stud), 
    path("meetform/",views.add_meet),
    path("mentorform/",views.add_mentor),
    path("locform/",views.add_loc),
    path("thesisform/",views.add_thesis),
    path("courseform/",views.add_course),
    path("adminform/",views.add_admin),
    path("vivaform/",views.add_viva),
    path("centerform/",views.add_center),
    path("report/",views.repo),
    path("reportstd/",views.repos),
    


    

     
]