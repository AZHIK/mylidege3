import os
# from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from django.core.exceptions import ValidationError
from django.conf import settings
import pycountry
from django.utils import timezone

CURRENT_EDUCATION_LEVEL_CHOICES = (
    ("A_level", "A_level"),
    ("O_level", "O_level"),
    ("Bachelor_degree", "Bachelor_degree"),
    ("Master_Degree", "Master_Degree"),
)

ADDMISSION_STATUS = (
    ("Approved","Approved"),
    ("Rejected","Rejected"), 
)

APPLYING_EDUCATION_LEVEL_CHOICES = (
    ("Bachelor Degree", "Bachelor Degree"),
    ("Master_Degree", "Master_Degree"),
    ("PHD", "PHD"),
)

def default_submission_time():
    return timezone.now()

class SubmissionTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None and add:
            value = timezone.now()
            setattr(model_instance, self.attname, value)  # Set the value on the instance
        return super().pre_save(model_instance, add)
    

# Define constants
PDF_EXTENSIONS = ['.pdf']
MAX_FILE_SIZE_MB = 5  # in megabytes

# Custom validator for file extension and size
def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    if not ext.lower() in PDF_EXTENSIONS:
        raise ValidationError('Only PDF files are allowed.')
    if value.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise ValidationError('File size cannot exceed 5MB.')

# Custom FileField with validation
class LimitedFileField(models.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('validators', [])
        kwargs['validators'].append(validate_file_extension)
        super().__init__(*args, **kwargs)

# Your models with LimitedFileField
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=True, null=True)
    username = models.CharField(max_length=100, unique=True)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='referrals')
    def __str__(self):
        return self.username
    class Meta:
        verbose_name_plural = "Users"


class Applicant_Personal_Details(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='personal_details')
    firstname = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    date_of_birth =  models.DateField(null=True)
    submission_time = SubmissionTimeField(null=True)

    nationality = models.CharField(
        max_length=100,
        choices=[(country.name, country.name) for country in pycountry.countries],
        blank=True,
        null=True,
    )  
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)

    def get_profile_image_url(self):
        if self.profile_image and hasattr(self.profile_image, 'url'):
            return self.profile_image.url
        else:
            return os.path.join(settings.MEDIA_URL, 'default.jpg')

    class Meta:
        verbose_name_plural = "Applicant personal Details"

class Applicants_guardian_details(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='guardian_details')
    
    fathername = models.CharField(max_length=100, null=True, blank=True)
    mothername = models.CharField(max_length=100, null=True, blank=True)
    next_of_kin = models.CharField(max_length=100)
    next_of_kin_relationship = models.CharField(max_length=100)
    next_of_kin_phone = models.CharField(max_length=13)
    next_of_kin_email = models.EmailField(null=True)
    next_of_kin_country = models.CharField(
        max_length=100,
        choices=[(country.name, country.name) for country in pycountry.countries],
        blank=True,
        null=True,
    )
    next_of_kin_city = models.CharField(max_length=13)
    next_of_kin_postal_code = models.CharField(max_length=13,null=True, blank=True)
    next_of_kin_profile_image = models.ImageField(upload_to='profile_images/',null=True, blank=True)
    submission_time = SubmissionTimeField(null=True)  

    def get_next_of_kin_profile_image_url(self):
        if self.profile_image and hasattr(self.next_of_kin_profile_image, 'url'):
            return self.next_of_kin_profile_image.url
        else:
            return os.path.join(settings.MEDIA_URL, 'default_image.jpg') 
    class Meta:
        verbose_name_plural = "Guardian Details"

class Applicants_academic_qualification(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='academic_qualifications')
    level_of_education = models.CharField(choices=CURRENT_EDUCATION_LEVEL_CHOICES, max_length=20,default="A_Level")
    certificate_file = LimitedFileField(upload_to='certificates/')
    results_transcripts = LimitedFileField(upload_to='transcripts/',null=True, blank=True)
    school_name = models.CharField(max_length=100)
    program = models.CharField(max_length=100)
    passing_year = models.IntegerField(default=2020)
    submission_time = SubmissionTimeField(null=True)

    class Meta:
        verbose_name_plural = "Academic Qualifications"

class Applicant_Selections(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='selections')
    education_level = models.CharField(choices=APPLYING_EDUCATION_LEVEL_CHOICES, max_length=20,default="Bachelor_Degree")
    interested_university1 = models.CharField(max_length=100)
    interested_university2 = models.CharField(max_length=100)
    interested_university3 = models.CharField(max_length=100)
    interested_university4 = models.CharField(max_length=100)
    interested_country1 = models.CharField(max_length=100,
        choices=[(country.name, country.name) for country in pycountry.countries],
        blank=True,
        null=True,)
    interested_country2 = models.CharField(max_length=100,
        choices=[(country.name, country.name) for country in pycountry.countries],
        blank=True,
        null=True,)
    interested_country3 = models.CharField(max_length=100,
        choices=[(country.name, country.name) for country in pycountry.countries],
        blank=True,
        null=True,)
    interested_country4 = models.CharField(max_length=100,
        choices=[(country.name, country.name) for country in pycountry.countries],
        blank=True,
        null=True,)
    interested_courses1 = models.CharField(max_length=100)
    interested_courses2 = models.CharField(max_length=100)
    interested_courses3 = models.CharField(max_length=100)
    interested_courses4 = models.CharField(max_length=100)
    submission_time = SubmissionTimeField(null=True)

    class Meta:
        verbose_name_plural = "Applicant Selections"

class Applicant_Other_Qualifications(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='other_qualifications')
    professional_Qualifications = models.TextField(null=True, blank=True)
    language_proficiency = models.CharField(max_length=10,null=True, blank=True)
    working_expirience = models.IntegerField(null=True, blank=True)
    computer_literacy = models.CharField(max_length=255,null=True, blank=True)
    CV_document = LimitedFileField(upload_to='transcripts/',null=True, blank=True)
    training_or_workshop1 = models.CharField(max_length=300,null=True, blank=True)
    training_or_workshop2 = models.CharField(max_length=300,null=True, blank=True)
    training_or_workshop3 = models.CharField(max_length=300,null=True, blank=True)
    other_attachments1 = LimitedFileField(upload_to='otherAttachments/',null=True, blank=True)
    other_attachments2 = LimitedFileField(upload_to='otherAttachments/',null=True, blank=True)
    other_attachments3 = LimitedFileField(upload_to='otherAttachments/',null=True, blank=True)
    training_and_workshops = LimitedFileField(upload_to='otherAttachments/',null=True, blank=True)
    submission_time = SubmissionTimeField(null=True)

class Addmitted_student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='addmitted_student')
    addmitted_university = models.CharField(max_length=100)
    country_selected = models.CharField(max_length=100,
        choices=[(country.name, country.name) for country in pycountry.countries],
        blank=True,
        null=True,)
    allocated_progrramme = models.CharField(max_length=100)
    addmission_date = models.DateField(null=True)
    hostel_fees_payment_reciept = LimitedFileField(upload_to='payment_reciepts/fees/')
    tuition_fees_payment_reciept = LimitedFileField(upload_to='payment_reciepts/fees/')
    Other_payment_reciept = LimitedFileField(upload_to='payment_reciepts/fees/')
    addmission_leter = LimitedFileField(upload_to='addmission_letter/', null=True)
    feedback = models.TextField()
    submission_time = SubmissionTimeField(null=True)
    addmission_approval = models.CharField(choices=ADDMISSION_STATUS, max_length=50, null=True)
    addmission_reject_reason = models.TextField(null=True)


