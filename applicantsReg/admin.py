from django.contrib import admin
from .models import CustomUser, Applicant_Personal_Details, Applicants_guardian_details,Applicants_academic_qualification, Applicant_Selections, Applicant_Other_Qualifications, Addmitted_student 

from django.utils.html import mark_safe


class UserAdmin(admin.ModelAdmin):
    list_display = ["id","username", "email"]

class Applicant_Personal_Details_Admin(admin.ModelAdmin):
    list_display = ["firstname", "last_name","date_of_birth","nationality", "phone","profile_image"]
    def get_profile_image(self, obj):
         
         if obj.profile_image and hasattr(obj.profile_image, 'url'):
            return mark_safe(f'<img src="{obj.profile_image.url}" width="50" height="50" />')
         else:
            return "No image uploaded"

class Applicants_guardian_details_Admin(admin.ModelAdmin):
     list_display = ["fathername", "mothername","next_of_kin","next_of_kin_phone","next_of_kin_email", "next_of_kin_country","next_of_kin_city","next_of_kin_relationship","next_of_kin_city",
         "next_of_kin_postal_code"]

class Applicants_academic_qualification_Admin(admin.ModelAdmin):
     list_display = ["level_of_education","certificate_file","results_transcripts","school_name","program","passing_year"]

class Applicant_selections_Admin(admin.ModelAdmin):
     list_display = ["education_level",
         "interested_university1",
         "interested_university2",
         "interested_university3",
         "interested_university4",
         "interested_country1",
         "interested_country2",
         "interested_country3",
         "interested_country4",
         "interested_courses1",
         "interested_courses2",
         "interested_courses3",
         "interested_courses4",]


class Applicant_Other_Qualifications_Admin(admin.ModelAdmin):
     list_display = [
         "professional_Qualifications", 
         "working_expirience",
         "computer_literacy",
         "CV_document",
         "training_or_workshop1",
         "training_or_workshop2",
         "training_or_workshop3",
         "other_attachments1", 
         "other_attachments2" ,
         "other_attachments3", 
         ]


class Addmitted_student_Admin(admin.ModelAdmin):
     list_display = [
         "addmitted_university",
         "country_selected", 
         "allocated_progrramme", 
         "hostel_fees_payment_reciept", 
         "tuition_fees_payment_reciept", 
         "Other_payment_reciept",
         "feedback",
           ]


admin.site.register(CustomUser,UserAdmin)
admin.site.register(Applicant_Personal_Details,Applicant_Personal_Details_Admin)
admin.site.register(Applicants_guardian_details,Applicants_guardian_details_Admin)
admin.site.register(Applicants_academic_qualification,Applicants_academic_qualification_Admin)
admin.site.register(Applicant_Selections,Applicant_selections_Admin)
admin.site.register(Applicant_Other_Qualifications,Applicant_Other_Qualifications_Admin)
admin.site.register(Addmitted_student,Addmitted_student_Admin)