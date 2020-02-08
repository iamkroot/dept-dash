from django.urls import path
from .api.faculty import *
from .api.hod import *
from .api.student import *

urlpatterns = [
    # Student
    path('api/lor/student/editProfile', EditProfile.as_view()),
    path('api/lor/student/uploadPicture', UploadProfilePicture.as_view()),
    path('api/lor/student/viewProfile', GetMyProfile.as_view()),
    path('api/lor/student/getProfilePicture', GetMyProfilePicture.as_view()),
    path('api/lor/student/createLor', CreateLor.as_view()),
    path('api/lor/student/editLor/<int:lor_id>', EditLor.as_view()),
    path('api/lor/student/selectFaculty', AddFacultyForLOR.as_view()),
    path('api/lor/student/editSubmittedLor/<int:faculty>/<int:lor>', EditSubmittedLorCourseDetails.as_view()),
    path('api/lor/student/getSavedLor', GetMySavedLor.as_view()),
    path('api/lor/student/getSavedLorForApplication', GetLorForApplication.as_view()),
    path('api/lor/student/getFacultyList', GetFacultyList.as_view()),
    path('api/lor/student/home', GetAppliedLor.as_view()),
    path('api/lor/student/getUnivList', GetUnivList.as_view()),
    path('api/lor/student/getAppliedLor', GetAppliedLor.as_view()),
    path('api/lor/student/getProfilePhoto', ViewProfilePhoto.as_view()),
    path('api/lor/student/deleteLor/<int:lor_id>', DeleteLor.as_view()),
    path('api/lor/student/withdrawApplication/<int:faculty>/<int:lor>', WithdrawApplications.as_view()),
    # HOD
    path('api/lor/hod/getAllAcceptedRequests', GetAcceptedEntriesHod.as_view()),
    path('api/lor/hod/getAllNewRequests', GetAllNewRequestsHod.as_view()),
    path('api/lor/hod/getAllCompletedRequests', GetAllCompletedRequestsHod.as_view()),
    path('api/lor/hod/getAllRequests', GetAllRequests.as_view()),
    path('api/lor/hod/home', GetHodHome.as_view()),
    path('api/lor/hod/getAllStudents', GetAllStudents.as_view()),
    # path('api/lor/hod/activeUserControl', GetActiveUsers.as_view()),
    path('api/lor/hod/getProfilePhoto/<int:student_id>', GetStudentProfilePhoto.as_view()),
    # Faculty
    path('api/lor/faculty/home', GetHome.as_view()),
    path('api/lor/faculty/getLorAcceptData', GetLorAcceptData.as_view()),
    path('api/lor/faculty/getAcceptedLorData', AcceptedLorData.as_view()),
    path('api/lor/faculty/acceptLor/<int:lor>/<int:faculty>', AcceptLorRequest.as_view()),
    path('api/lor/faculty/rejectLor/<int:lor>/<int:faculty>', RejectLorRequest.as_view()),
    path('api/lor/faculty/markAsComplete/<int:lor>/<int:faculty>', MarkRequestAsComplete.as_view()),
    path('api/lor/faculty/getProfilePhoto/<int:student_id>', GetStudentProfilePhoto.as_view()),
    path('api/lor/faculty/completedLorData', CompletedLorData.as_view()),
]
