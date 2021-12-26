from django import forms
from django.forms import fields
from .models import centerloc, mentorform, stuform,meetform, thesisform,vivaform,courseform,adminform,centerform


class studForm(forms.ModelForm):
	class Meta:
		model = stuform
		fields = ['student_id','student_first_name','student_last_name',
				'phone_number', 'age', 'duration_of_phd', 'status_of_phd',
				'university', 'mentor_id', 'student_email','meeting_id','center_no']

class meetForm(forms.ModelForm):
      class Meta:
            model = meetform
            fields =['Meeting_ID','Student_First_Name','Date_of_Meeting1','Date_of_Meeting2','Student_Email']

class thesisForm(forms.ModelForm):
      class Meta:
            model = thesisform
            fields =['student_id','student_first_name','thesis_submission_status','date_of_submission']
class vivaForm(forms.ModelForm):
      class Meta:
            model = vivaform
            fields =['student_id','student_first_name','viva_status','pcv_status','cv_status']
class courseForm(forms.ModelForm):
      class Meta:
            model = courseform
            fields =['course_id','student_id','student_first_name','instructor_first_name','instructor_last_name','course_name']
class adminForm(forms.ModelForm):
      class Meta:
            model = adminform
            fields =['hall_ticket_no','student_id','student_first_name','document_status','admission_quota','interview_status']
class centerForm(forms.ModelForm):
      class Meta:
            model = centerform
            fields =['center_no','student_id','student_first_name','incharge_first_name','incharge_last_name']
class mentorForm(forms.ModelForm):
      class Meta:
            model = mentorform
            fields =['mentor_id','student_id','student_first_name','mentor_first_name','mentor_last_name','mentor_phno','mentor_age','mentor_email']
class locForm(forms.ModelForm):
      class Meta:
            model = centerloc
            fields =['center_no','student_id','student_first_name','city_name','state']



	# 	def clean(self):
      #       super(studForm, self).clean()

      # # getting username and password from cleaned_data
      #       stu_id = self.cleaned_data.get('stu_id')
      #       sfn  = self.cleaned_data.get('sfn')
	# 		sln = self.cleaned_data.get('sln')
      #       phno = self.cleaned_data.get('phno')

      # # validating the username and password
      #       if len(sfn) < 5:
      #          self._errors['sfn'] = self.error_class(['A minimum of 5 characters is required'])

      #       if len(sln) < 8:
      #          self._errors['sln'] = self.error_class(['Password length should not be less than 8 characters'])

      #       return self.cleaned_data
