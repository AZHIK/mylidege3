from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserRegistrationForm,ApproveAddmissionForm,AddmittedStudentForm, ApplicantOtherQualificationsForm, ApplicantSelectionsForm, ApplicantsAcademicQualificationForm, ApplicantsGuardianDetailsForm, ApplicantPersonalDetailsForm
from .models import CustomUser, Applicant_Personal_Details, Applicants_guardian_details, Applicants_academic_qualification, Applicant_Selections, Applicant_Other_Qualifications, Addmitted_student
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.contrib.auth import get_user_model


def register(request):
    if request.user.is_authenticated:
        return redirect("startApplication")
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            referred_by_username = request.GET.get('referral_username')
            if referred_by_username:
                referred_by_user = CustomUser.objects.filter(username=referred_by_username).first()
                if referred_by_user:
                    user.referred_by = referred_by_user
            user.save()
            Applicant_Personal_Details.objects.create(user=user)
            Applicants_guardian_details.objects.create(user=user)
            Applicants_academic_qualification.objects.create(user=user)
            Applicant_Selections.objects.create(user=user)
            Applicant_Other_Qualifications.objects.create(user=user)
            Addmitted_student.objects.create(user=user)
            login(request, user)
            return redirect("startApplication")
    else:
        form = UserRegistrationForm()
        
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("applist")
        else:
            return redirect("applicant_details")
        
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect("applist")
                else:
                    return redirect("profile")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def is_staff(user):
    return user.is_staff


def is_admin(user):
    return user.is_authenticated and user.is_superuser


@login_required
@user_passes_test(is_staff)
def generate_referral_link(request):
    if not request.user.is_authenticated:
        return redirect("login")

    CustomUser = get_user_model()
    username = request.user.username
    registration_url = reverse('register')
    referral_link = request.build_absolute_uri(f"{registration_url}?referral_username={username}")
    return render(request, 'referral_link.html', {'referral_link': referral_link})


def applicant_details_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.is_staff:
        return redirect("applist")
    
    applicant_details = getattr(request.user, 'personal_details', None)
    if applicant_details:
        submission_time = applicant_details.submission_time  # Assuming there's a submission_time field in your model
        if applicant_details is not None and submission_time is not None:
            if submission_time + timedelta(hours=168) < timezone.now():  # Assuming there's a submission_time field in your model
                messages.warning(request, "You can't modify your data after 24 hours since submission.")
                return redirect("home")
        if request.method == "POST":
            form = ApplicantPersonalDetailsForm(request.POST, request.FILES, instance=applicant_details)
            if form.is_valid():
                form.save()
                return redirect('guardian')
        else:
            form = ApplicantPersonalDetailsForm(instance=applicant_details)
        return render(request, "personalDetails.html", {"form": form,"applicant_details":applicant_details , "messages":messages})
    else:
        messages.warning(request, "You don't have any profile. Please contact your system admin.")
        return redirect("home")


def startApplication(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request,'startRegistration.html')


def guardian_details_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.is_staff:
        return redirect("applist")
    applicant_details = getattr(request.user, 'personal_details', None)
    guardian_details = getattr(request.user, 'guardian_details', None)
    
    if guardian_details:
        submission_time = guardian_details.submission_time  # Assuming there's a submission_time field in your model
        if guardian_details is not None and submission_time is not None:
            if submission_time + timedelta(hours=168) < timezone.now():  # Assuming there's a submission_time field in your model
                messages.warning(request, "You can't modify your data after 24 hours since submission.")
                return redirect("home")
        if request.method == "POST":
            form = ApplicantsGuardianDetailsForm(request.POST, request.FILES, instance=guardian_details)
            if form.is_valid():
                form.save()
                return redirect('academics')
        else:
            form = ApplicantsGuardianDetailsForm(instance = guardian_details)
        return render(request, "guardianDetails.html", {"form": form,"applicant_details":applicant_details,"messages":messages})
    else:
        error_message = "You don't have any profile you may logout or contact you system admin."
        messages.warning(request, error_message)
        return redirect("home")


def academic_qualification_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.is_staff:
        return redirect("applist")
    applicant_details = getattr(request.user, 'personal_details', None)
    academic_qualification = getattr(request.user, 'academic_qualifications', None)
    if academic_qualification:
        submission_time = academic_qualification.submission_time
        if academic_qualification is not None and submission_time is not None:
            if submission_time + timedelta(hours=168) < timezone.now():  # Assuming there's a submission_time field in your model
                messages.warning(request, "You can't modify your data after 24 hours since submission.")
                return redirect("home")
        if request.method == "POST":
            form = ApplicantsAcademicQualificationForm(request.POST, request.FILES, instance=academic_qualification)
            if form.is_valid():
                form.save()
                return redirect('selections')
        else:
            form = ApplicantsAcademicQualificationForm(instance = academic_qualification)
        return render(request, "academics.html", {"form": form,"applicant_details":applicant_details,"messages":messages})
    else:
        error_message = "You don't have any profile you may logout or contact you system admin."
        messages.warning(request, error_message)
        return redirect("home")
    


def selections_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.is_staff:
        return redirect("applist")
    applicant_details = getattr(request.user, 'personal_details', None)
    selections  = getattr(request.user, 'selections', None)
    if selections:
        submission_time = selections.submission_time  # Assuming there's a submission_time field in your model
        if selections is not None and submission_time is not None:
            if submission_time + timedelta(hours=168) < timezone.now():  # Assuming there's a submission_time field in your model
                messages.warning(request, "You can't modify your data after 24 hours since submission.")
                return redirect("home")
        if request.method == "POST":
            form = ApplicantSelectionsForm(request.POST, request.FILES, instance=selections)
            if form.is_valid():
                form.save()
                return redirect('other')
        else:
            form = ApplicantSelectionsForm(instance = selections)
        return render(request, "selections.html", {"form": form,"applicant_details":applicant_details,"messages":messages})
    else:
        error_message = "You don't have any profile you may logout or contact you system admin."
        messages.warning(request, error_message)
        return redirect("home")



def other_qualifications_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    applicant_details = getattr(request.user, 'personal_details', None)
    if request.user.is_staff:
        return redirect("applist")
    other_qualifications   = getattr(request.user, 'other_qualifications', None)
    
    if other_qualifications :
        submission_time = other_qualifications.submission_time  # Assuming there's a submission_time field in your model
        if other_qualifications is not None and submission_time is not None:
            if submission_time + timedelta(hours=168) < timezone.now():  # Assuming there's a submission_time field in your model
                messages.warning(request, "You can't modify your data after 24 hours since submission.")
                return redirect("home")
        
        if request.method == "POST":
            form = ApplicantOtherQualificationsForm(request.POST, request.FILES, instance = other_qualifications )
            if form.is_valid():
                form.save()
                return redirect('profile')
        else:
            form = ApplicantOtherQualificationsForm(instance = other_qualifications)
        return render(request, "otherQualifications.html", {"form": form,"applicant_details":applicant_details,"messages":messages})
    else:
        error_message = "You don't have any profile you may logout or contact you system admin."
        messages.warning(request, error_message)
        return redirect("home")


@user_passes_test(is_staff)
def addmitted_student_view(request,user):
    if not request.user.is_authenticated:
        return redirect("login")
    addmitted = Addmitted_student.objects.get(user = user)
    if addmitted :
        if request.method == "POST":
            form = AddmittedStudentForm(request.POST, request.FILES, instance = addmitted )
            if form.is_valid():
                feedback = form.save(commit=False)
                feedback.addmitted = addmitted
                feedback.save()
                messages.success(request, "successfull submitted")
        else:
            form = AddmittedStudentForm(instance = addmitted)
        return render(request, "addmission.html", {"form": form, "addmitted":addmitted,"messages":messages})
    else:
        error_message = "You don't have any profile you may logout or contact you system admin."
        messages.warning(request, error_message)
        return redirect("home")



def approve_addmission(request,user):
    if not request.user.is_authenticated:
        return redirect("login")
    addmitted = Addmitted_student.objects.get(user = user)
    addmitted.addmission_approval = "Approved"
    addmitted.save()
    return redirect("addmission_status_staff",user = user)


def reject_addmission(request,user):
    if not request.user.is_authenticated:
        return redirect("login")
    addmitted = Addmitted_student.objects.get(user = user)
    addmitted.addmission_approval = "Rejected"
    addmitted.save()
    return redirect("addmission_status_staff",user = user)



@user_passes_test(is_staff)
def addmission_status(request,user):
    if not request.user.is_authenticated:
        return redirect("login")
    applicantDetails = Applicant_Personal_Details.objects.get(user = user)
    addmitted = Addmitted_student.objects.get(user = user)
    if addmitted :
        return render(request,'addmssion_status_for_staff.html',{"addmitted":addmitted,"applicantDetails":applicantDetails})


def applicant_details_display_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.is_staff:
        return redirect("applist")
    applicant_details = getattr(request.user, 'personal_details', None)
    guardian_details = getattr(request.user, 'guardian_details', None)
    academic_qualification = getattr(request.user, 'academic_qualifications', None)
    selections  = getattr(request.user, 'selections', None)
    other_qualifications   = getattr(request.user, 'other_qualifications', None)
    

    if applicant_details or selections or guardian_details or academic_qualification or selections or other_qualifications:

        context = {
            "applicant_details":applicant_details,
            "guardian_details":guardian_details, 
            "academic_qualification":academic_qualification, 
            "selections": selections, 
            "other_qualifications":other_qualifications, 
                    }

        return render(request, "profile_view.html",context)
    else:
        error_message = "You don't have any profile you may logout or contact you system admin."
        messages.warning(request, error_message)
        return redirect("home")



@user_passes_test(is_staff)
def applicant_list(request):
    if not request.user.is_authenticated:
        return redirect("login")
    myusers = CustomUser.objects.all()
    applicantDetails = Applicant_Personal_Details.objects.all()
    addmittedStud = Addmitted_student.objects.all()

    if applicantDetails or addmittedStud :

        context = {
              "myusers":myusers,
              "applicant_details":applicantDetails,
               "addmitted":addmittedStud   
             }

        return render(request, "applicantList.html",context)
    

@user_passes_test(is_staff)
def applicant_view(request,user):
    if not request.user.is_authenticated:
        return redirect("login")
    applicantDetails = Applicant_Personal_Details.objects.get(user = user)
    addmittedStud = Addmitted_student.objects.get(user = user)
    guardian_details = Applicants_guardian_details.objects.get(user = user)
    academic_qualification = Applicants_academic_qualification.objects.get(user = user)
    selections  = Applicant_Selections.objects.get(user = user)
    other_qualifications   = Applicant_Other_Qualifications.objects.get(user = user)

    if applicantDetails or selections or guardian_details or academic_qualification or selections or other_qualifications or addmittedStud:

        context = {
              "applicant_details":applicantDetails,
               "addmitted":addmittedStud,
               "guardian_details":guardian_details,
               "academic_qualification":academic_qualification,
               "selections":selections,
               "other_qualifications":other_qualifications,
               "addmittedStud":addmittedStud
             }

        return render(request, "userinfo.html",context)


def addmission_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    addmitted = getattr(request.user, 'addmitted_student', None)
    applicant_details = getattr(request.user, 'personal_details', None)
    if addmitted or applicant_details:
        context={
            "applicant_details":applicant_details,
            "addmitted":addmitted
        }

    return render(request,'addmission_status.html',context)


def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("applist")
        else:
            return redirect("profile")   
    return render(request,'homepage.html')

def logout_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    logout(request)
    return redirect("home")


