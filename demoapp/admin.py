from django.contrib import admin
from .models import Student,Mentor,courses, meetform, thesisform,viva,thesis,meetings,stuform,meetform, vivaform,courseform,adminform,centerform,mentorform,centerloc
from import_export.admin import ImportExportModelAdmin
 

admin.site.register(Student)
admin.site.register(Mentor)
admin.site.register(courses)

@admin.register(viva)
@admin.register(thesis)
@admin.register(meetings)
@admin.register(stuform)
@admin.register(meetform)
@admin.register(thesisform)
@admin.register(courseform)
@admin.register(vivaform)
@admin.register(adminform)
@admin.register(centerform)
@admin.register(mentorform)
@admin.register(centerloc)
class hello(ImportExportModelAdmin):
        pass
admin.register(viva)
admin.register(thesis)
admin.register(meetings)
admin.register(stuform)
admin.register(meetform)
admin.register(thesisform)
admin.register(vivaform)
admin.register(courseform)
admin.register(adminform)
admin.register(centerform)
admin.register(mentorform)
admin.register(centerloc)





