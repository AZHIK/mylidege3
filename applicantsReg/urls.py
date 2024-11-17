from django.urls import path
from . import views


urlpatterns = [
    path('', views.home,name = 'home'),
    path('register/',views.register,name = 'register'),
    path('login/',views.login_view,name = 'login'),
    path('applicant_details/',views.applicant_details_view,name = 'applicant_details'),
    path('guardian/',views.guardian_details_view,name = 'guardian'),
    path('academics/',views.academic_qualification_view,name = 'academics'),
    path('startApplication/', views.startApplication , name = 'startApplication'),
    path('selections/',views.selections_view,name = 'selections'),
    path('other/',views.other_qualifications_view,name = 'other'),
    path('addmission/<user>',views.addmitted_student_view,name = 'addmission'),
    path('addmission_status/',views.addmission_view, name = 'addmission_status' ),
    path('addmission_status_staff/<user>',views.addmission_status, name = 'addmission_status_staff' ),
    path('applist/',views.applicant_list,name = 'applist'),
    path('approve/<user>',views.approve_addmission,name = 'approve'),
    path('reject/<user>',views.reject_addmission,name = 'reject'),
    path('appview/<user>',views.applicant_view,name = 'appview'),
    path('profile/',views.applicant_details_display_view,name = 'profile'),
    path('logout/', views.logout_view , name = 'logout'  ),
    path('refferal/', views.generate_referral_link , name = 'refferal')
                ]