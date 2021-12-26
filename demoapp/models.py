from django.db import models
import re


class Student(models.Model):
    sid =models.IntegerField(primary_key=True)
    FN =models.CharField(max_length=20)
    MN =models.CharField(max_length=20)
    LN =models.CharField(max_length=20)
    phno =models.CharField(max_length=13)
    age =models.IntegerField()
    duration =models.CharField(max_length=20)
    status_phd =models.CharField(max_length=20)
    university =models.CharField(max_length=20)
    mid =models.IntegerField()
    st_email =models.CharField(max_length=50)
    meet_id =models.IntegerField()
    center_no =models.IntegerField()
    def __str__(self):
        return self.FN
class Mentor(models.Model):
    mid =models.IntegerField(primary_key=True)
    mfn =models.CharField(max_length=20)
    mln =models.CharField(max_length=20)
    m_phno =models.CharField(max_length=13)
    m_age =models.IntegerField()
    m_email =models.CharField(max_length=50)
    def __str__(self):
        return self.mfn
class mentorform(models.Model):
    mentor_id =models.IntegerField(primary_key=True)
    student_id =models.IntegerField()
    student_first_name =models.CharField(max_length=20)
    mentor_first_name =models.CharField(max_length=20)
    mentor_last_name =models.CharField(max_length=20)
    mentor_phno =models.CharField(max_length=13)
    mentor_age =models.IntegerField()
    mentor_email =models.CharField(max_length=50)
    def __str__(self):
        return self.mentor_first_name 
class centerloc(models.Model):
    center_no =models.IntegerField(primary_key=True)
    student_id =models.IntegerField()
    student_first_name =models.CharField(max_length=20)
    city_name =models.CharField(max_length=13)
    state =models.CharField(max_length=50)
    def __str__(self):
        return self.city_name
class courses(models.Model):
    course_id =models.IntegerField(primary_key=True)
    c_inst_fn =models.CharField(max_length=20)
    c_inst_ln =models.CharField(max_length=20)
    course_name =models.CharField(max_length=13)
    sid =models.IntegerField()
    def __str__(self):
        return self.course_name
class courseform(models.Model):
    course_id =models.IntegerField(primary_key=True)
    student_id =models.IntegerField()
    student_first_name= models.CharField(max_length=20)
    instructor_first_name =models.CharField(max_length=20)
    instructor_last_name =models.CharField(max_length=20)
    course_name =models.CharField(max_length=13)
    def __str__(self):
        return self.course_name
class adminform(models.Model):
    hall_ticket_no =models.IntegerField(primary_key=True)
    student_id =models.IntegerField()
    student_first_name= models.CharField(max_length=20)
    document_status = models.CharField(max_length=20)
    admission_quota = models.CharField(max_length=20)
    interview_status = models.CharField(max_length=20)
    def __str__(self):
        return self.student_first_name
class centerform(models.Model):
    center_no =models.IntegerField()
    student_id =models.IntegerField(primary_key=True)
    student_first_name= models.CharField(max_length=20)
    incharge_first_name = models.CharField(max_length=20)
    incharge_last_name = models.CharField(max_length=20)
    def __str__(self):
        return self.student_first_name
class viva(models.Model):
    sid =models.IntegerField(primary_key=True)
    FN =models.CharField(max_length=20)
    viva_status =models.CharField(max_length=20)
    pcv_or_cv =models.CharField(max_length=20)
    pcv_status=models.CharField(max_length=13)
    cv_status =models.CharField(max_length=20)
    def __str__(self):
        return self.FN
class vivaform(models.Model):
    student_id =models.IntegerField(primary_key=True)
    student_first_name =models.CharField(max_length=20)
    viva_status =models.CharField(max_length=20)
    pcv_status=models.CharField(max_length=13)
    cv_status =models.CharField(max_length=20)
    def __str__(self):
        return self.student_first_name
class thesisform(models.Model):
    student_id =models.IntegerField(primary_key=True)
    student_first_name =models.CharField(max_length=20)
    thesis_submission_status =models.CharField(max_length=20)
    date_of_submission =models.CharField(max_length=20)
    def __str__(self):
        return self.student_first_name
class meetings(models.Model):
    FN =models.CharField(max_length=20)
    meet_id =models.IntegerField(primary_key=True)
    date1 =models.DateField(max_length=20)
    date2 =models.DateField(max_length=20)
    def __str__(self):
        return self.FN
class meetform(models.Model):
    Meeting_ID =models.IntegerField(primary_key=True)
    Student_First_Name =models.CharField(max_length=20)
    Date_of_Meeting1 =models.DateField(max_length=20)
    Date_of_Meeting2 =models.DateField(max_length=20)
    Student_Email = models.EmailField(max_length=60)
    def __str__(self):
        return self.Student_First_Name
class thesis(models.Model):
    sid =models.IntegerField(primary_key=True)
    FN =models.CharField(max_length=20)
    thesis_submission_status =models.CharField(max_length=20)
    date_of_submission =models.CharField(max_length=20)
    def __str__(self):
        return self.FN
# def validate_sfn(value):
                                                                      
#     pattern = re.compile(r"[[0-9]+")                                                
                                                                                                                    
                                                                                
#     if pattern.search(value):                                                        
#        raise ValidationError('%s is a number' % value)                                                      
                                                     
       

class stuform(models.Model):
    student_id =models.IntegerField(primary_key=True)
    student_first_name =models.CharField(max_length=20)
    # smn =models.CharField(max_length=20)
    student_last_name =models.CharField(max_length=20)
    phone_number =models.CharField(max_length=13)
    age =models.IntegerField()
    duration_of_phd =models.CharField(max_length=20)
    status_of_phd =models.CharField(max_length=20)
    university =models.CharField(max_length=20)
    mentor_id =models.IntegerField()
    student_email =models.CharField(max_length=50)
    meeting_id =models.IntegerField()
    center_no =models.IntegerField()
    def __str__(self):
        return self.sfn



