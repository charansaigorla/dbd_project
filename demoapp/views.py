from contextlib import redirect_stderr
from django.shortcuts import render,redirect
from django.contrib.auth import login as auth_login,authenticate ,logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#from .models import tbl_Authentication
from django.contrib import messages
from django.http import FileResponse
from django.http import HttpResponseRedirect
from .forms import CreateUserForm
from django.contrib import messages
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from .models import Student, centerloc,courses,Mentor,meetings, mentorform, stuform,meetform,thesisform,vivaform
from .forms import adminForm, centerForm, courseForm, locForm, mentorForm, studForm,meetForm,thesisForm,vivaForm,courseform,adminform,centerform
from fpdf import FPDF
from firstproject import settings
from django.core.mail import send_mail
from django.db import connection

#from demo.firstproject.demoapp import forms
# Create your views here.

   
def home(request):
    return render(request,'base.html')
def repo(request):
    return render(request,'reports.html')
def repos(request):
    return render(request,'reportstud.html')
def student(request):
    post1 = mentorform.objects.all()
    post2 = courseform.objects.all()
    return render(request,"student.html",{"post1":post1,"post2":post2})
def mentor(request):
    post = stuform.objects.all()
    post3 = meetform.objects.all()
    return render(request,'mentor.html',{"post":post,"post3":post3})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        email = request.POST.get('email')
        print('Username',username)
        print('Password',pass1)
        print('Email',email)
        user = authenticate(username=username,password=pass1)
        print('User details',user)
        if user is not None:
            print('gorla')
            auth_login(request,user)
            print('gorla')
            #fname = user.fist_name
            n = len(email)
            for i in range(n):
                if email[i] is '.':
                    return redirect(student)
                if email[i] == '@':
                    return redirect(mentor)

            return redirect(mentor)     
        else:
            print('charan sai chowdary')
            messages.error(request,"Wrong Credentials")
            return redirect(home)
    
    return render(request,'login.html')
def register(request):
    if request.method=='POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        address = request.POST.get('address') 
        print(address)
        phno = request.POST.get('phno')
        print(phno)
        myuser = User.objects.create_user(username=username,password=pass1,email=email)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.address = address
        myuser.password = pass1
        myuser.phno = phno

        myuser.save()
        messages.success(request,"Created!")
        return redirect(login)

    return render(request,'register.html')
def lgout(request):
    logout(request)
    messages.success(request,"Logged out Successfully")
    return redirect(home)
def regis(request):
#    if request.user.is_authenticated:
#        return redirect(login)
#    else: 
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,'Account created for '+user)
                return redirect(login)

        context={'form':form}
        return render(request,'registerform.html',context)
def student_pdf(request):
    buf=io.BytesIO()
    c=canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob=c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",14)

    # lines = [
    #     "This is line 1",
    #     "This is line 2",
    #     "This is line 3",
    # ]
    
    
    l=[]

    st = Student.objects.all()
 
    # lines.append("Mentor Details")
    # lines.append("=========================")
    # for venue in venues:
    #     lines.append(str(venue.mid))
    #     lines.append(str(venue.mfn))
    #     lines.append(str(venue.mln))
    #     lines.append(str(venue.m_phno))
    #     lines.append(str(venue.m_age))
    #     lines.append(str(venue.m_email))
    #     lines.append("=========================")
    l.append(" Student Details")
    l.append("=========================")
    for s in st:
        l.append(str(s.sid))
        l.append(str(s.FN))
        l.append(str(s.MN))
        l.append(str(s.LN))
        l.append(str(s.phno))
        l.append(str(s.age))
        l.append(str(s.duration))
        l.append(str(s.status_phd))
        l.append(str(s.university))
        l.append(str(s.mid))
        l.append(str(s.st_email))
        l.append(str(s.meet_id))
        l.append(str(s.center_no))

        l.append("=========================")
        
    
    # for l in lines:
    #     textob.textLine(line)
    for p in l:
        textob.textLine(p)
        

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='student.pdf')


# Create your views here.
# def add_stud(request):
# 	form = studForm(request.POST or None)
# 	if form.is_valid():
# 		form.save()
# 	context = {
# 		"form": form,
# 		"title": "New Student",
# 	}
# 	return render(request, "studentform.html", context)
def add_stud(request):
    if request.method == 'POST':
       form = studForm(request.POST or None)
       if form.is_valid():
        form.save()
        phoneno = form.cleaned_data.get('phone_number') 
        age = form.cleaned_data.get('age') 
        centorno = form.cleaned_data.get('centor_no') 
        meetid = form.cleaned_data.get('meeting_id') 
        if len(phoneno)!= 10:
            messages.error(request,'Enter valid phone number')
            connection.cursor().execute("DELETE FROM demoapp_stuform WHERE phone_number = %s",[phoneno])
            return render(request, "studentform.html", {"form":form})
        elif(age<15):
            messages.error(request,'Invalid Age')
            connection.cursor().execute("DELETE FROM demoapp_stuform WHERE age = %s",[age])
            return render(request, "studentform.html", {"form":form})
        elif(centorno<10000):
            messages.error(request,'Invalid center number')
            connection.cursor().execute("DELETE FROM demoapp_stuform WHERE center_no = %s",[centorno])
            return render(request, "studentform.html", {"form":form})
        elif(meetid<100):
            messages.error(request,'Invalid meet id')
            connection.cursor().execute("DELETE FROM demoapp_stuform WHERE meeting_id = %s",[meetid])
            return render(request, "studentform.html", {"form":form})
        else:
            return render(request,"student.html")
    else:
       form = studForm()
       context = {
		"form": form,
		"title": "New Meeting",
	  }

    return render(request, "studentform.html", context)

def add_thesis(request):
    if request.method == 'POST':
      form = thesisForm(request.POST or None)
      if form.is_valid():
        form.save()
        return render(request,"student.html")
    else:
        form = thesisForm()
        context = {
		  "form": form,
		"title": "New Meeting",
	    }
    return render(request, "thesisform.html", context)
def add_viva(request):
    if request.method == 'POST':
      form = vivaForm(request.POST or None)
      if form.is_valid():
        form.save()
        return render(request,"student.html")
    else:
        form = vivaForm()
        context = {
		  "form": form,
		"title": "New Meeting",
	    }
    return render(request, "vivaform.html", context)
def add_course(request):
	form = courseForm(request.POST or None)
	if form.is_valid():
		form.save()
        

	context = {
		"form": form,
		"title": "New Record",
	}
	return render(request, "courseform.html", context)
# def add_course(request):
#    # if request.method == 'POST':
#        form = courseForm(request.POST or None)
#        if form.is_valid():
#           form.save()
#           courseid = form.cleaned_data.get('course_id') 
#           if courseid<=1000:
#             messages.error(request,'Course ID should be above 1000')
#             connection.cursor().execute("DELETE FROM demoapp_courseform WHERE course_id = %s",[courseid])
#             return render(request, "courseform.html", {"form":form})
#         #   else:
#         #     return render(request,"student.html") 

#         context = {
# 		  "form": form,
# 		  "title": "New Meeting",
# 	    }

#        return render(request, "courseform.html", context)

def add_admin(request):
    if request.method == 'POST':
      form = adminForm(request.POST or None)
      if form.is_valid():
        form.save()
        return render(request,"student.html")
    else:
        form = adminForm()
        context = {
		  "form": form,
		"title": "New Meeting",
	    }
    return render(request, "admission.html", context)
# def add_center(request):
# 	form = centerForm(request.POST or None)
# 	if form.is_valid():
# 		form.save()
# 	context = {
# 		"form": form,
# 		"title": "New Record",
# 	}
# 	return render(request, "centerform.html", context)
def add_center(request):
    if request.method == 'POST':
       form = centerForm(request.POST or None)
       if form.is_valid():
            form.save()
            centerno = form.cleaned_data.get('center_no')
            if(centerno<10000):
                messages.error(request,'Center Number should be above 10000')
                connection.cursor().execute("DELETE FROM demoapp_centerform WHERE center_no = %s",[centerno])
                return render(request, "centerform.html", {"form":form})
            else:
                return render(request,"student.html") 

    else:
        form = centerForm()
        context = {
		  "form": form,
		"title": "New Meeting",
	    }

    return render(request, "centerform.html", context)
        
        
   

# def add_mentor(request):
# 	form = mentorForm(request.POST or None)
# 	if form.is_valid():
# 		form.save()
        
# 	context = {
# 		"form": form,
# 		"title": "New Record",
# 	}
# 	return render(request, "mentorform.html", context)
def add_mentor(request):
    if request.method == 'POST':
      form = mentorForm(request.POST or None)
      if form.is_valid():
        form.save()
        mentorphno = form.cleaned_data.get('mentor_phno')
        if len(mentorphno) != 10 or int(mentorphno)<1:
            messages.error(request,'Enter valid phone number')
            connection.cursor().execute("DELETE FROM demoapp_mentorform WHERE mentor_phno = %s",[mentorphno])
            return render(request, "mentorform.html", {"form":form})
        else:
            return render(request,"student.html") 

    else:
        form = mentorForm()
        context = {
		  "form": form,
		"title": "New Meeting",
	    }

    return render(request, "mentorform.html", context)
       
   

def add_loc(request):
    if request.method == 'POST':
      form = locForm(request.POST or None)
      if form.is_valid():
        form.save()
        return render(request,"mentor.html")
    else:
        form = locForm()
        context = {
		  "form": form,
		"title": "New Meeting",
	    }
    return render(request, "locform.html", context)
# def add_meet(request):
# 	form = meetForm(request.POST or None)
# 	if form.is_valid():
# 		form.save()
# 	context = {
# 		"form": form,
# 		"title": "New Meeting",
# 	}
# 	return render(request, "meetform.html", context)
def add_meet(request):
   #if request.method == 'POST':
    form = meetForm(request.POST or None)
    if form.is_valid():
        form.save()
        meetid = form.cleaned_data.get('Meeting_ID') 
        stufn = form.cleaned_data.get('Student_First_Name') 
        date1 = form.cleaned_data.get('Date_of_Meeting1') 
        date2 = form.cleaned_data.get('Date_of_Meeting2') 
        date1 = str(date1)
        date2 = str(date2)
        meetid = str(meetid)
        email= form.cleaned_data.get('Student_Email')
        subject = "Details Regarding Doctorial Meetings"
        message = "Hello\t"+stufn+"\n"+"Your doctorial meetings are scheduled on\t"+date1+"\tand\t"+date2+" respectively with meeting ID"+meetid+". Kindly attend positively\n\nThank you"
        from_email = settings.EMAIL_HOST_USER
        to_list = [email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)
       # return render(request,"mentor.html")
    #else:
        #form = meetForm()
    context = {
		"form": form,
		"title": "New Meeting",
	    }

    return render(request, "meetform.html", context)

def student_report(request):
    sales = [
        {'student_id':'hello','student_first_name':'charan','student_last_name':'sai','phone_number':'6789098712','age':'23','duration_of_phd':'comp','status_of_phd':'comp','university':'vtu','mentor_id':'5','student_email':'h@'},
        {'student_id':'','student_first_name':'','student_last_name':'','phone_number':'','age':'','duration_of_phd':'','status_of_phd':'','university':'','mentor_id':'','student_email':''},
        {'student_id':'','student_first_name':'','student_last_name':'','phone_number':'','age':'','duration_of_phd':'','status_of_phd':'','university':'','mentor_id':'','student_email':''},
        {'student_id':'','student_first_name':'','student_last_name':'','phone_number':'','age':'','duration_of_phd':'','status_of_phd':'','university':'','mentor_id':'','student_email':''},
        {'student_id':'','student_first_name':'','student_last_name':'','phone_number':'','age':'','duration_of_phd':'','status_of_phd':'','university':'','mentor_id':'','student_email':''},
        {'student_id':'','student_first_name':'','student_last_name':'','phone_number':'','age':'','duration_of_phd':'','status_of_phd':'','university':'','mentor_id':'','student_email':''},
        {'student_id':'','student_first_name':'','student_last_name':'','phone_number':'','age':'','duration_of_phd':'','status_of_phd':'','university':'','mentor_id':'','student_email':''},
        {'student_id':'','student_first_name':'','student_last_name':'','phone_number':'','age':'','duration_of_phd':'','status_of_phd':'','university':'','mentor_id':'','student_email':''},
        {'student_id':'','student_first_name':'','student_last_name':'','phone_number':'','age':'','duration_of_phd':'','status_of_phd':'','university':'','mentor_id':'','student_email':''},
        {'student_id':'','student_first_name':'','student_last_name':'','phone_number':'','age':'','duration_of_phd':'','status_of_phd':'','university':'','mentor_id':'','student_email':''},

       
    ]
    st = stuform.objects.all();
    lis = [
        {},{},{},{},{},{},{},
    ]
    i=0
    for s in st:
        sales[i]['student_id'] = str(s.student_id)
        sales[i]['student_first_name']= str(s.student_first_name)
        sales[i]['student_last_name']=str(s.student_last_name)
        sales[i]['phone_number']=str(s.phone_number)
        sales[i]['age']=str(s.age)
        sales[i]['duration_of_phd']=str(s.duration_of_phd)
        sales[i]['status_of_phd']=str(s.status_of_phd)
        sales[i]['university']=str(s.university)
        sales[i]['mentor_id']=str(s.mentor_id)
        sales[i]['student_email']=str(s.student_email)
        i=i+1
        # l.append(str(s.duration))
        # l.append(str(s.status_phd))
        # l.append(str(s.university))
        # l.append(str(s.mid))
        # l.append(str(s.st_email))
        # l.append(str(s.meet_id))
        # l.append(str(s.center_no))


    pdf = FPDF('L', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 16)
    pdf.cell(40, 10, 'Details of PhD Students',0,1)
    pdf.cell(40, 10, '',0,1)
    pdf.set_font('courier', '', 12)
    pdf.cell(200, 8, f"{'ID'.ljust(3)} {'FirstName'.ljust(7)} {'LastName'.ljust(7)} {'PhoneNumber'.ljust(7)} {'Age'.ljust(7)} {'DurationOfPhD'.ljust(3)} {'StatusOfPhD'.ljust(7)} {'University'.ljust(7)} {'MentorId'.ljust(9)} {'Email'.ljust(17)} ", 0, 1)
    pdf.line(10, 30, 290, 30)
    pdf.line(10, 38, 290, 38)
    for line in sales:
        pdf.cell(200, 8, f"{line['student_id'].ljust(3)} {line['student_first_name'].ljust(7)}  {line['student_last_name'].ljust(10)} {line['phone_number'].ljust(10)} {line['age'].ljust(10)} {line['duration_of_phd'].ljust(5)} {line['status_of_phd'].ljust(16)} {line['university'].ljust(7)} {line['mentor_id'].ljust(7)} {line['student_email'].ljust(3)}",0, 1)
    pdf.output('student_details.pdf', 'F')
    return FileResponse(open('student_details.pdf', 'rb'), as_attachment=True, content_type='application/pdf')
def meet_report(request):
    sales = [
        {'Meeting_ID':'hello','Student_First_Name':'charan','Date_of_Meeting1':'6789098712','Date_of_Meeting2':'23','Student_Email':''},
        {'Meeting_ID':'hello','Student_First_Name':'charan','Date_of_Meeting1':'6789098712','Date_of_Meeting2':'23','Student_Email':''},
        {'Meeting_ID':'hello','Student_First_Name':'charan','Date_of_Meeting1':'6789098712','Date_of_Meeting2':'23','Student_Email':''},
        {'Meeting_ID':'hello','Student_First_Name':'charan','Date_of_Meeting1':'6789098712','Date_of_Meeting2':'23','Student_Email':''},
        {'Meeting_ID':'hello','Student_First_Name':'charan','Date_of_Meeting1':'6789098712','Date_of_Meeting2':'23','Student_Email':''},
        {'Meeting_ID':'hello','Student_First_Name':'charan','Date_of_Meeting1':'6789098712','Date_of_Meeting2':'23','Student_Email':''},
        {'Meeting_ID':'hello','Student_First_Name':'charan','Date_of_Meeting1':'6789098712','Date_of_Meeting2':'23','Student_Email':''},
        {'Meeting_ID':'hello','Student_First_Name':'charan','Date_of_Meeting1':'6789098712','Date_of_Meeting2':'23','Student_Email':''},
        {'Meeting_ID':'hello','Student_First_Name':'charan','Date_of_Meeting1':'6789098712','Date_of_Meeting2':'23','Student_Email':''},
        {'Meeting_ID':'','Student_First_Name':'','Date_of_Meeting1':'','Date_of_Meeting2':'','Student_Email':''},
        {'Meeting_ID':'','Student_First_Name':'','Date_of_Meeting1':'','Date_of_Meeting2':'','Student_Email':''},
              {'Meeting_ID':'','Student_First_Name':'','Date_of_Meeting1':'','Date_of_Meeting2':'','Student_Email':''},
               {'Meeting_ID':'','Student_First_Name':'','Date_of_Meeting1':'','Date_of_Meeting2':'','Student_Email':''},
                {'Meeting_ID':'','Student_First_Name':'','Date_of_Meeting1':'','Date_of_Meeting2':'','Student_Email':''},
                 {'Meeting_ID':'','Student_First_Name':'','Date_of_Meeting1':'','Date_of_Meeting2':'','Student_Email':''},
                  {'Meeting_ID':'','Student_First_Name':'','Date_of_Meeting1':'','Date_of_Meeting2':'','Student_Email':''},
                   {'Meeting_ID':'','Student_First_Name':'','Date_of_Meeting1':'','Date_of_Meeting2':'','Student_Email':''},


       
    ]
    st = meetform.objects.all();
    lis = [
        {},{},{},{},{},{},{},
    ]
    i=0
    for s in st:
        sales[i]['Meeting_ID'] = str(s.Meeting_ID)
        sales[i]['Student_First_Name']= str(s.Student_First_Name)
        sales[i]['Date_of_Meeting1']=str(s.Date_of_Meeting1)
        sales[i]['Date_of_Meeting2']=str(s.Date_of_Meeting2)
        sales[i]['Student_Email']=str(s.Student_Email)
        i=i+1
        # l.append(str(s.duration))
        # l.append(str(s.status_phd))
        # l.append(str(s.university))
        # l.append(str(s.mid))
        # l.append(str(s.st_email))
        # l.append(str(s.meet_id))
        # l.append(str(s.center_no))


    pdf = FPDF('L', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 16)
    pdf.cell(40, 10, 'Details of Doctorial Meetings',0,1)
    pdf.cell(40, 10, '',0,1)
    pdf.set_font('courier', '', 12)
    pdf.cell(200, 8, f"{'Meeting_ID'.ljust(10)} {'FirstName'.ljust(10)}  {'Date_of_Meeting1'.ljust(10)} {'Date_of_Meeting2'.ljust(35)} {'Student_Email'.ljust(10)} ", 0, 1)
    pdf.line(10, 30, 290, 30)
    pdf.line(10, 38, 290, 38)
    for line in sales:
        pdf.cell(200, 8, f"{line['Meeting_ID'].ljust(10)} {line['Student_First_Name'].ljust(10)}   {line['Date_of_Meeting1'].ljust(20)} {line['Date_of_Meeting2'].ljust(20)} {line['Student_Email'].ljust(10)}",0, 1)
    pdf.output('meeting_details.pdf', 'F')
    return FileResponse(open('meeting_details.pdf', 'rb'), as_attachment=True, content_type='application/pdf')
def thesis_report(request):
    sales = [
        {'student_id':'','student_first_name':'','thesis_submission_status':'','date_of_submission':''},
        {'student_id':'','student_first_name':'','thesis_submission_status':'','date_of_submission':''},
        {'student_id':'','student_first_name':'','thesis_submission_status':'','date_of_submission':''},
        {'student_id':'','student_first_name':'','thesis_submission_status':'','date_of_submission':''},
        {'student_id':'','student_first_name':'','thesis_submission_status':'','date_of_submission':''},
        {'student_id':'','student_first_name':'','thesis_submission_status':'','date_of_submission':''},
        {'student_id':'','student_first_name':'','thesis_submission_status':'','date_of_submission':''},
        {'student_id':'','student_first_name':'','thesis_submission_status':'','date_of_submission':''},
        {'student_id':'','student_first_name':'','thesis_submission_status':'','date_of_submission':''},
                   


       
    ]
    st = thesisform.objects.all();
    lis = [
        {},{},{},{},{},{},{},
    ]
    i=0
    for s in st:
        sales[i]['student_id'] = str(s.student_id)
        sales[i]['student_first_name']= str(s.student_first_name)
        sales[i]['thesis_submission_status']=str(s.thesis_submission_status)
        sales[i]['date_of_submission']=str(s.date_of_submission)
        i=i+1
        # l.append(str(s.duration))
        # l.append(str(s.status_phd))
        # l.append(str(s.university))
        # l.append(str(s.mid))
        # l.append(str(s.st_email))
        # l.append(str(s.meet_id))
        # l.append(str(s.center_no))


    pdf = FPDF('L', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 16)
    pdf.cell(40, 10, 'Details of thesis',0,1)
    pdf.cell(40, 10, '',0,1)
    pdf.set_font('courier', '', 12)
    pdf.cell(200, 8, f"{'Student_ID'.ljust(10)} {'FirstName'.ljust(10)}  {'Thesis_Submission_Status'.ljust(10)} {'Date_of_Submission'.ljust(35)}", 0, 1)
    pdf.line(10, 30, 290, 30)
    pdf.line(10, 38, 290, 38)
    for line in sales:
        pdf.cell(200, 8, f"{line['student_id'].ljust(10)} {line['student_first_name'].ljust(10)}   {line['thesis_submission_status'].ljust(20)} {line['date_of_submission'].ljust(20)}",0, 1)
    pdf.output('thesis_details.pdf', 'F')
    return FileResponse(open('thesis_details.pdf', 'rb'), as_attachment=True, content_type='application/pdf')
def viva_report(request):
    sales = [
        {'student_id':'','student_first_name':'','viva_status':'','pcv_status':'','cv_status':''},
        {'student_id':'','student_first_name':'','viva_status':'','pcv_status':'','cv_status':''},
        {'student_id':'','student_first_name':'','viva_status':'','pcv_status':'','cv_status':''},
        {'student_id':'','student_first_name':'','viva_status':'','pcv_status':'','cv_status':''},
        {'student_id':'','student_first_name':'','viva_status':'','pcv_status':'','cv_status':''},
        {'student_id':'','student_first_name':'','viva_status':'','pcv_status':'','cv_status':''},



       
    ]
    st = vivaform.objects.all();
    lis = [
        {},{},{},{},{},{},{},
    ]
    i=0
    for s in st:
        sales[i]['student_id'] = str(s.student_id)
        sales[i]['student_first_name']= str(s.student_first_name)
        sales[i]['viva_status']=str(s.viva_status)
        sales[i]['pcv_status']=str(s.pcv_status)
        sales[i]['cv_status']=str(s.cv_status)
        i=i+1
        # l.append(str(s.duration))
        # l.append(str(s.status_phd))
        # l.append(str(s.university))
        # l.append(str(s.mid))
        # l.append(str(s.st_email))
        # l.append(str(s.meet_id))
        # l.append(str(s.center_no))


    pdf = FPDF('L', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 16)
    pdf.cell(40, 10, 'Details of Viva Status',0,1)
    pdf.cell(40, 10, '',0,1)
    pdf.set_font('courier', '', 12)
    pdf.cell(200, 8, f"{'Student_ID'.ljust(10)} {'FirstName'.ljust(10)}  {'Viva_Status'.ljust(10)} {'pcv_Status'.ljust(10)} {'cv_status'.ljust(35)}", 0, 1)
    pdf.line(10, 30, 290, 30)
    pdf.line(10, 38, 290, 38)
    for line in sales:
        pdf.cell(200, 8, f"{line['student_id'].ljust(10)} {line['student_first_name'].ljust(10)}  {line['viva_status'].ljust(20)} {line['pcv_status'].ljust(20)} {line['cv_status'].ljust(20)}",0, 1)
    pdf.output('thesis_details.pdf', 'F')
    return FileResponse(open('thesis_details.pdf', 'rb'), as_attachment=True, content_type='application/pdf')
def course_report(request):
    sales = [
        {'course_id':'','student_id':'','student_first_name':'','instructor_first_name':'','instructor_last_name':'','course_name':''},
        {'course_id':'','student_id':'','student_first_name':'','instructor_first_name':'','instructor_last_name':'','course_name':''},
        {'course_id':'','student_id':'','student_first_name':'','instructor_first_name':'','instructor_last_name':'','course_name':''},
        {'course_id':'','student_id':'','student_first_name':'','instructor_first_name':'','instructor_last_name':'','course_name':''},
        {'course_id':'','student_id':'','student_first_name':'','instructor_first_name':'','instructor_last_name':'','course_name':''},
        {'course_id':'','student_id':'','student_first_name':'','instructor_first_name':'','instructor_last_name':'','course_name':''},




       
    ]
    st = courseform.objects.all();
    lis = [
        {},{},{},{},{},{},{},
    ]
    i=0
    for s in st:
        sales[i]['course_id'] = str(s.course_id)
        sales[i]['student_id'] = str(s.student_id)
        sales[i]['student_first_name']= str(s.student_first_name)
        sales[i]['instructor_first_name']=str(s.instructor_first_name)
        sales[i]['instructor_last_name']=str(s.instructor_last_name)
        sales[i]['course_name']=str(s.course_name)
        i=i+1
        # l.append(str(s.duration))
        # l.append(str(s.status_phd))
        # l.append(str(s.university))
        # l.append(str(s.mid))
        # l.append(str(s.st_email))
        # l.append(str(s.meet_id))
        # l.append(str(s.center_no))


    pdf = FPDF('L', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 16)
    pdf.cell(40, 10, 'Details of Course',0,1)
    pdf.cell(40, 10, '',0,1)
    pdf.set_font('courier', '', 12)
    pdf.cell(200, 8, f"{'Course_ID'.ljust(10)} {'Student_ID'.ljust(10)} {'FirstName'.ljust(10)}  {'Instructor_first_name'.ljust(10)} {'Instructor_last_name'.ljust(10)} {'course_name'.ljust(35)}", 0, 1)
    pdf.line(10, 30, 290, 30)
    pdf.line(10, 38, 290, 38)
    for line in sales:
        pdf.cell(200, 8, f"{line['course_id'].ljust(10)} {line['student_id'].ljust(10)} {line['student_first_name'].ljust(10)}  {line['instructor_first_name'].ljust(20)} {line['instructor_last_name'].ljust(20)} {line['course_name'].ljust(20)}",0, 1)
    pdf.output('course_details.pdf', 'F')
    return FileResponse(open('course_details.pdf', 'rb'), as_attachment=True, content_type='application/pdf')
def admin_report(request):
    sales = [
        {'hall_ticket_no':'','student_id':'','student_first_name':'','document_status':'','admission_quota':'','interview_status':''},
        {'hall_ticket_no':'','student_id':'','student_first_name':'','document_status':'','admission_quota':'','interview_status':''},
        {'hall_ticket_no':'','student_id':'','student_first_name':'','document_status':'','admission_quota':'','interview_status':''},
        {'hall_ticket_no':'','student_id':'','student_first_name':'','document_status':'','admission_quota':'','interview_status':''},
        {'hall_ticket_no':'','student_id':'','student_first_name':'','document_status':'','admission_quota':'','interview_status':''},
        {'hall_ticket_no':'','student_id':'','student_first_name':'','document_status':'','admission_quota':'','interview_status':''},
        {'hall_ticket_no':'','student_id':'','student_first_name':'','document_status':'','admission_quota':'','interview_status':''},



       
    ]
    st = adminform.objects.all();
    lis = [
        {},{},{},{},{},{},{},
    ]
    i=0
    for s in st:
        sales[i]['hall_ticket_no'] = str(s.hall_ticket_no)
        sales[i]['student_id'] = str(s.student_id)
        sales[i]['student_first_name']= str(s.student_first_name)
        sales[i]['document_status']=str(s.document_status)
        sales[i]['admission_quota']=str(s.admission_quota)
        sales[i]['interview_status']=str(s.interview_status)
        i=i+1
        # l.append(str(s.duration))
        # l.append(str(s.status_phd))
        # l.append(str(s.university))
        # l.append(str(s.mid))
        # l.append(str(s.st_email))
        # l.append(str(s.meet_id))
        # l.append(str(s.center_no))


    pdf = FPDF('L', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 16)
    pdf.cell(40, 10, 'Details of Admission',0,1)
    pdf.cell(40, 10, '',0,1)
    pdf.set_font('courier', '', 12)
    pdf.cell(200, 8, f"{'hall_ticket_no'.ljust(10)} {'Student_ID'.ljust(10)} {'FirstName'.ljust(10)}  {'Document_Status'.ljust(10)} {'admission_Status'.ljust(10)} {'interview_status'.ljust(35)}", 0, 1)
    pdf.line(10, 30, 290, 30)
    pdf.line(10, 38, 290, 38)
    for line in sales:
        pdf.cell(200, 8, f"{line['hall_ticket_no'].ljust(10)} {line['student_id'].ljust(10)} {line['student_first_name'].ljust(10)}  {line['document_status'].ljust(20)} {line['admission_quota'].ljust(20)} {line['interview_status'].ljust(20)}",0, 1)
    pdf.output('admission_details.pdf', 'F')
    return FileResponse(open('admission_details.pdf', 'rb'), as_attachment=True, content_type='application/pdf')
def center_report(request):
    sales = [
        {'center_no':'','student_id':'','student_first_name':'','incharge_first_name':'','incharge_last_name':''},
        {'center_no':'','student_id':'','student_first_name':'','incharge_first_name':'','incharge_last_name':''},
        {'center_no':'','student_id':'','student_first_name':'','incharge_first_name':'','incharge_last_name':''},
        {'center_no':'','student_id':'','student_first_name':'','incharge_first_name':'','incharge_last_name':''},
        {'center_no':'','student_id':'','student_first_name':'','incharge_first_name':'','incharge_last_name':''},
        {'center_no':'','student_id':'','student_first_name':'','incharge_first_name':'','incharge_last_name':''},
        {'center_no':'','student_id':'','student_first_name':'','incharge_first_name':'','incharge_last_name':''},




       
    ]
    st = centerform.objects.all();
    lis = [
        {},{},{},{},{},{},{},
    ]
    i=0
    for s in st:
        sales[i]['center_no'] = str(s.center_no)
        sales[i]['student_id'] = str(s.student_id)
        sales[i]['student_first_name']= str(s.student_first_name)
        sales[i]['incharge_first_name']=str(s.incharge_first_name)
        sales[i]['incharge_last_name']=str(s.incharge_last_name)
        i=i+1
        # l.append(str(s.duration))
        # l.append(str(s.status_phd))
        # l.append(str(s.university))
        # l.append(str(s.mid))
        # l.append(str(s.st_email))
        # l.append(str(s.meet_id))
        # l.append(str(s.center_no))


    pdf = FPDF('L', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 16)
    pdf.cell(40, 10, 'Details of Center',0,1)
    pdf.cell(40, 10, '',0,1)
    pdf.set_font('courier', '', 12)
    pdf.cell(200, 8, f"{'Center_no'.ljust(10)} {'Student_ID'.ljust(10)} {'FirstName'.ljust(10)}  {'Incharge_first_name'.ljust(10)} {'Incharge_last_name'.ljust(10)}", 0, 1)
    pdf.line(10, 30, 290, 30)
    pdf.line(10, 38, 290, 38)
    for line in sales:
        pdf.cell(200, 8, f"{line['center_no'].ljust(10)} {line['student_id'].ljust(10)} {line['student_first_name'].ljust(10)}  {line['incharge_first_name'].ljust(20)} {line['incharge_last_name'].ljust(20)}",0, 1)
    pdf.output('center_details.pdf', 'F')
    return FileResponse(open('center_details.pdf', 'rb'), as_attachment=True, content_type='application/pdf')
def mentor_report(request):
    sales = [
        {'mentor_id':'','student_id':'','student_first_name':'','mentor_first_name':'','mentor_last_name':'','mentor_phno':'','mentor_age':'','mentor_email':''},
        {'mentor_id':'','student_id':'','student_first_name':'','mentor_first_name':'','mentor_last_name':'','mentor_phno':'','mentor_age':'','mentor_email':''},
        {'mentor_id':'','student_id':'','student_first_name':'','mentor_first_name':'','mentor_last_name':'','mentor_phno':'','mentor_age':'','mentor_email':''},
        {'mentor_id':'','student_id':'','student_first_name':'','mentor_first_name':'','mentor_last_name':'','mentor_phno':'','mentor_age':'','mentor_email':''},
        {'mentor_id':'','student_id':'','student_first_name':'','mentor_first_name':'','mentor_last_name':'','mentor_phno':'','mentor_age':'','mentor_email':''},
        {'mentor_id':'','student_id':'','student_first_name':'','mentor_first_name':'','mentor_last_name':'','mentor_phno':'','mentor_age':'','mentor_email':''},
        {'mentor_id':'','student_id':'','student_first_name':'','mentor_first_name':'','mentor_last_name':'','mentor_phno':'','mentor_age':'','mentor_email':''},
        {'mentor_id':'','student_id':'','student_first_name':'','mentor_first_name':'','mentor_last_name':'','mentor_phno':'','mentor_age':'','mentor_email':''},





       
    ]
    st = mentorform.objects.all();
    lis = [
        {},{},{},{},{},{},{},
    ]
    i=0
    for s in st:
        sales[i]['mentor_id'] = str(s.mentor_id)
        sales[i]['student_id'] = str(s.student_id)
        sales[i]['student_first_name']= str(s.student_first_name)
        sales[i]['mentor_first_name']=str(s.mentor_first_name)
        sales[i]['mentor_last_name']=str(s.mentor_last_name)
        sales[i]['mentor_phno']=str(s.mentor_phno)
        sales[i]['mentor_age']=str(s.mentor_age)
        sales[i]['mentor_email']=str(s.mentor_email)
        i=i+1
        # l.append(str(s.duration))
        # l.append(str(s.status_phd))
        # l.append(str(s.university))
        # l.append(str(s.mid))
        # l.append(str(s.st_email))
        # l.append(str(s.meet_id))
        # l.append(str(s.center_no))


    pdf = FPDF('L', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 16)
    pdf.cell(40, 10, 'Details of Mentor',0,1)
    pdf.cell(40, 10, '',0,1)
    pdf.set_font('courier', '', 12)
    pdf.cell(200, 8, f"{'Mentor_ID'.ljust(10)} {'Student_ID'.ljust(10)} {'FirstName'.ljust(10)}  {'mentor_first_name'.ljust(10)} {'mentor_last_name'.ljust(10)} {'mentor_phno'.ljust(10)} {'mentor_age'.ljust(10)} {'mentor_email'.ljust(10)}  ", 0, 1)
    pdf.line(10, 30, 290, 30)
    pdf.line(10, 38, 290, 38)
    for line in sales:
        pdf.cell(200, 8, f"{line['mentor_id'].ljust(10)} {line['student_id'].ljust(10)} {line['student_first_name'].ljust(10)}  {line['mentor_first_name'].ljust(20)} {line['mentor_last_name'].ljust(20)} {line['mentor_phno'].ljust(20)} {line['mentor_age'].ljust(20)} {line['mentor_email'].ljust(20)}",0, 1)
    pdf.output('mentor_details.pdf', 'F')
    return FileResponse(open('mentor_details.pdf', 'rb'), as_attachment=True, content_type='application/pdf')
def location_report(request):
    sales = [
        {'center_no':'','student_id':'','student_first_name':'','city_name':'','state':''},
        {'center_no':'','student_id':'','student_first_name':'','city_name':'','state':''},
        {'center_no':'','student_id':'','student_first_name':'','city_name':'','state':''},
        {'center_no':'','student_id':'','student_first_name':'','city_name':'','state':''},
        {'center_no':'','student_id':'','student_first_name':'','city_name':'','state':''},
        {'center_no':'','student_id':'','student_first_name':'','city_name':'','state':''},
        {'center_no':'','student_id':'','student_first_name':'','city_name':'','state':''},




       
    ]
    st = centerloc.objects.all();
    lis = [
        {},{},{},{},{},{},{},
    ]
    i=0
    for s in st:
        sales[i]['center_no'] = str(s.center_no)
        sales[i]['student_id'] = str(s.student_id)
        sales[i]['student_first_name']= str(s.student_first_name)
        sales[i]['city_name']=str(s.city_name)
        sales[i]['state']=str(s.state)
        i=i+1
        # l.append(str(s.duration))
        # l.append(str(s.status_phd))
        # l.append(str(s.university))
        # l.append(str(s.mid))
        # l.append(str(s.st_email))
        # l.append(str(s.meet_id))
        # l.append(str(s.center_no))


    pdf = FPDF('L', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 16)
    pdf.cell(40, 10, 'Details of Center Location',0,1)
    pdf.cell(40, 10, '',0,1)
    pdf.set_font('courier', '', 12)
    pdf.cell(200, 8, f"{'Center_no'.ljust(10)} {'Student_ID'.ljust(10)} {'FirstName'.ljust(10)}  {'City_name'.ljust(10)} {'State'.ljust(10)}", 0, 1)
    pdf.line(10, 30, 290, 30)
    pdf.line(10, 38, 290, 38)
    for line in sales:
        pdf.cell(200, 8, f"{line['center_no'].ljust(10)} {line['student_id'].ljust(10)} {line['student_first_name'].ljust(10)}  {line['city_name'].ljust(20)} {line['state'].ljust(20)}",0, 1)
    pdf.output('location_details.pdf', 'F')
    return FileResponse(open('location_details.pdf', 'rb'), as_attachment=True, content_type='application/pdf')
