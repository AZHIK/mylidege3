from django import forms
import pycountry
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Applicant_Personal_Details, Applicants_guardian_details,Applicants_academic_qualification, Applicant_Selections, Applicant_Other_Qualifications, Addmitted_student


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(),
    )
    username = forms.CharField(
       label='Username',
       help_text="" ,
       widget=forms.TextInput(),
    )
    

    password1 = forms.CharField(
        label="password",
        widget=forms.PasswordInput(),
        help_text="Password must be at least 8 characters long and not too common.",
    )
    password2 = forms.CharField(
        label="confirm password",
        widget=forms.PasswordInput(),
        help_text="",
    )

class ApplicantPersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = Applicant_Personal_Details
        fields = ("firstname", "last_name","date_of_birth","nationality", "phone","profile_image")
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type':'date'})
        }
    pass

class ApplicantsGuardianDetailsForm(forms.ModelForm):
    class Meta:
        model = Applicants_guardian_details
        fields = ("fathername", "mothername","next_of_kin","next_of_kin_phone","next_of_kin_email", "next_of_kin_country","next_of_kin_city","next_of_kin_relationship")
    pass

class ApplicantsAcademicQualificationForm(forms.ModelForm):
    class Meta:
        model = Applicants_academic_qualification
        fields = ("level_of_education","certificate_file","results_transcripts","school_name","program","passing_year")
    pass

class ApplicantSelectionsForm(forms.ModelForm):
    class Meta:
        model = Applicant_Selections
        fields = (
        "education_level",
        "interested_university1",
        "interested_university2",
        "interested_university3",
        "interested_country1",
        "interested_country2",
        "interested_country3",
        "interested_courses1",
        "interested_courses2",
        "interested_courses3",
        )
    
    interested_university1 = forms.CharField(
       label='University',
       help_text="" ,
       widget=forms.TextInput(),
    )
    interested_university2 = forms.CharField(
       label='University',
       help_text="" ,
       widget=forms.TextInput(),
    )
    interested_university3 = forms.CharField(
       label='University',
       help_text="" ,
       widget=forms.TextInput(),
    )

    
    interested_country1 = forms.ChoiceField(
        choices=[(country.name, country.name) for country in pycountry.countries],
        label='Country',
        help_text="" 
    )
    interested_country2 = forms.ChoiceField(
        choices=[(country.name, country.name) for country in pycountry.countries],
       label='Country',
       help_text="" ,
       )
    interested_country3 = forms.ChoiceField(
        choices=[(country.name, country.name) for country in pycountry.countries],
       label='Country',
       help_text="" ,
    )

    interested_courses1 = forms.CharField(
       label='Programme',
       help_text="" ,
       widget=forms.TextInput(),
    )
    interested_courses2 = forms.CharField(
       label='Programme',
       help_text="" ,
       widget=forms.TextInput(),
    )
    interested_courses3 = forms.CharField(
       label='Programme',
       help_text="" ,
       widget=forms.TextInput(),
    )



class ApplicantOtherQualificationsForm(forms.ModelForm):
    class Meta:
        model = Applicant_Other_Qualifications
        fields = (
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
        )
    training_or_workshop1 = forms.CharField(
       label='training/workshop tittle',
       help_text="" ,
       widget=forms.TextInput(),
       required = False
    )
    training_or_workshop2 = forms.CharField(
       label='training/workshop tittle',
       help_text="" ,
       widget=forms.TextInput(),
       required = False
    )
    training_or_workshop3 = forms.CharField(
       label='training/workshop tittle',
       help_text="" ,
       widget=forms.TextInput(),
       required = False
    )

    other_attachments1 = forms.FileField(
       label='attachment',
       help_text="" ,
       required = False
    )

    other_attachments2 = forms.FileField(
       label='attachment',
       help_text="" ,
       required = False
    )
    other_attachments3 = forms.FileField(
       label='attachment',
       help_text="" ,
       required = False
    )

class AddmittedStudentForm(forms.ModelForm):
    class Meta:
        model = Addmitted_student
        fields = (
        "addmitted_university",
        "country_selected", 
        "allocated_progrramme", 
        "hostel_fees_payment_reciept", 
        "tuition_fees_payment_reciept", 
        "Other_payment_reciept",
        "addmission_leter",
        "feedback", 
        )
    country_selected = forms.ChoiceField(
        choices=[(country.name, country.name) for country in pycountry.countries],
       label='Country',
       help_text="" ,
    )

class ApproveAddmissionForm(forms.ModelForm):
    class Meta:
        model = Addmitted_student
        fields = (
         "addmission_approval",   
        ) 