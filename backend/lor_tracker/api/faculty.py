# Create your views here.
import base64
import json
import os
from datetime import timezone

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.serializers import serialize
from django.http import HttpResponse
from django.template import Template, Context
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import *
from lor_tracker.serializers import *
from backend.settings import BASE_DIR
from backend.settings import EMAIL_HOST_USER

ACCEPT_TEMPLATE = """
Dear {{student.full_name}}:

Your Letter of Recommendation request to Professor {{faculty.first_name}} {{faculty.last_name}}, has been accepted.
For further communication with the faculty, please contact {{faculty.email}}.

Best Regards,
Head of the Department
Departments of Computer Science and Information Systems

For any query or inconvenience related to accessing the site please email to lor@hyderabad.bits-pilani.ac.in
"""

REJECT_TEMPLATE = """
Dear {{student.full_name}}:

Your Letter of Recommendation request to Professor {{faculty.first_name}} {{faculty.last_name}}, has been rejected.
For further communication with the faculty, please contact {{faculty.email}}.

Best Regards,
Head of the Department
Departments of Computer Science and Information Systems

For any query or inconvenience related to accessing the site please email to lor@hyderabad.bits-pilani.ac.in
"""

COMPLETE_TEMPLATE = """
Dear {{student.full_name}}:

Your Letter of Recommendation request to Professor {{faculty.first_name}} {{faculty.last_name}}, has been completed.
Please check your related application portal.

For further communication with the faculty, please contact {{faculty.email}}.

Best Regards,
Head of the Department
Departments of Computer Science and Information Systems

For any query or inconvenience related to accessing the site please email to lor@hyderabad.bits-pilani.ac.in
"""


# Get Home Data for faculty
class GetHome(APIView):
    permission_classes = [IsFaculty]
    
    # serializer_class = StudentProfileSerializer
    def get(self, request):
        result = {}
        new_requests = FacultyListLor.objects.filter(faculty=self.request.user.psrn, application_status='AP')
        accepted_requests = FacultyListLor.objects.filter(faculty=self.request.user.psrn, application_status='AC')
        completed_requests = FacultyListLor.objects.filter(faculty=self.request.user.psrn, application_status='CO')
        result["newRequests"] = len(new_requests)
        result["acceptedRequests"] = len(accepted_requests)
        result["completedRequests"] = len(completed_requests)
        deadline_content = []
        for item in accepted_requests:
            lor_details = Lor.objects.get(id=item.lor.id)
            # data = json.loads(serialize('json', lor_details))[0]["fields"]
            # print(data)
            # print(lor_details.deadline)
            diff = (lor_details.deadline - datetime.now(timezone.utc)).days
            # print(diff)
            if 5 >= diff >= 0:
                details = {}
                user_details = Student.objects.get(id_num=lor_details.user.id_num)
                details["student_details_general"] = GetStudentSerializer(user_details).data
                details["student_details_profile"] = StudentProfileSerializer(
                    StudentDetails.objects.get(user=lor_details.user.id_num)).data
                details["lor_details"] = ViewSavedLor(lor_details).data
                details["application_details"] = ViewAppliedFacultyListSerializer(
                    FacultyListLor.objects.get(faculty_id=self.request.user.psrn, lor_id=lor_details.id)).data
                deadline_content.append(details)
        result["upcomingDeadlines"] = deadline_content
        print(result)
        return Response(result)


class GetLorAcceptData(APIView):
    permission_classes = [
        IsFaculty
    ]
    
    # serializer_class = StudentProfileSerializer
    def get(self, request):
        result = []
        new_requests = FacultyListLor.objects.filter(faculty=self.request.user.psrn, application_status='AP')
        print(new_requests)
        for item in new_requests:
            print(item.lor.user.id_num)
            details = {}
            print(StudentDetails.objects.filter(user=item.lor.user), item)
            lor_details = json.loads(serialize('json', Lor.objects.filter(id=item.lor.id)))[0]["fields"]
            user_details = Student.objects.values("id_num", "email", "name").get(
                id_num=item.lor.user.id_num)
            profile_details = json.loads(serialize('json', StudentDetails.objects.filter(user=item.lor.user)))[0][
                "fields"]
            details["student_details_general"] = user_details
            details["lor_details"] = lor_details
            details["student_details_profile"] = profile_details
            details["application_details"] = json.loads(serialize('json', FacultyListLor.objects.filter
            (faculty=self.request.user.psrn, application_status='AP', lor=item.lor.id)))[0]["fields"]
            result.append(details)
        return Response(result)


class AcceptedLorData(APIView):
    permission_classes = [
        IsFaculty
    ]
    
    # serializer_class = StudentProfileSerializer
    def get(self, request):
        result = []
        new_requests = FacultyListLor.objects.filter(faculty=self.request.user.psrn, application_status='AC')
        print(new_requests)
        for item in new_requests:
            print(item.lor.user.id)
            details = {}
            print(StudentDetails.objects.filter(user=item.lor.user), item)
            lor_details = json.loads(serialize('json', Lor.objects.filter(id=item.lor.id)))[0]["fields"]
            user_details = Student.objects.values("id_num", "email", "name").get(id_num=item.lor.user.id_num)
            profile_details = json.loads(serialize('json', StudentDetails.objects.filter(user=item.lor.user)))[0][
                "fields"]
            details["student_details_general"] = user_details
            details["lor_details"] = lor_details
            details["student_details_profile"] = profile_details
            details["application_details"] = json.loads(serialize('json', FacultyListLor.objects.filter
            (faculty=self.request.user.psrn, application_status='AC', lor=item.lor.id)))[0]["fields"]
            result.append(details)
        return Response(result)


class AcceptLorRequest(APIView):
    permission_classes = [
        IsFaculty
    ]
    
    # serializer_class = StudentProfileSerializer
    def get(self, request, lor, faculty):
        lor_details = Lor.objects.get(id=lor)
        details = StudentDetails.objects.values("full_name", "phone").get(user=lor_details.user.id)
        student_mail = Student.objects.values("id_num", "email").get(id_num=lor_details.user.id_num)
        faculty_details = Faculty.objects.values("name", "email").get(psrn=faculty)
        template = Template(ACCEPT_TEMPLATE)
        send_mail(
            'Your LOR Request has been Accepted',
            template.render(context=Context({'faculty': faculty_details, 'student': details})),
            EMAIL_HOST_USER,
            [student_mail['email']],
            fail_silently=False,
        )
        result = FacultyListLor.objects.filter(lor=lor, faculty=faculty).update(application_status='AC')
        return Response(result)


class RejectLorRequest(APIView):
    permission_classes = [
        IsFaculty
    ]
    
    # serializer_class = StudentProfileSerializer
    def get(self, request, lor, faculty):
        lor_details = Lor.objects.get(id=lor)
        details = StudentDetails.objects.values("full_name", "phone").get(user=lor_details.user.id)
        student_mail = Student.objects.values("id_num", "email").get(id_num=lor_details.user.id_num)
        faculty_details = Faculty.objects.values("name", "email").get(psrn=faculty)
        template = Template(REJECT_TEMPLATE)
        send_mail(
            'Your LOR Request has been Rejected',
            template.render(context=Context({'faculty': faculty_details, 'student': details})),
            EMAIL_HOST_USER,
            [student_mail.email],
            fail_silently=False,
        )
        result = FacultyListLor.objects.filter(lor=lor, faculty=faculty).update(application_status='RE')
        return Response(result)


class MarkRequestAsComplete(APIView):
    permission_classes = [
        IsFaculty
    ]
    
    def get(self, request, lor, faculty):
        lor_details = Lor.objects.get(id=lor)
        details = StudentDetails.objects.values("full_name", "phone").get(user=lor_details.user.id)
        student_mail = Student.objects.values("id_num", "email").get(id_num=lor_details.user.id_num)
        faculty_details = Faculty.objects.values("name", "email").get(psrn=faculty)
        template = Template(COMPLETE_TEMPLATE)
        send_mail(
            'Your Letter of Recommendation is Ready',
            template.render(context=Context({'faculty': faculty_details, 'student': details})),
            EMAIL_HOST_USER,
            [student_mail["email"]],
            fail_silently=False,
        )
        result = FacultyListLor.objects.filter(lor=lor, faculty=faculty).update(application_status='CO')
        return Response(result)


class CompletedLorData(APIView):
    permission_classes = [
        IsFaculty
    ]
    
    # serializer_class = StudentProfileSerializer
    def get(self, request):
        result = []
        new_requests = FacultyListLor.objects.filter(faculty=self.request.user.psrn, application_status='CO')
        print(new_requests)
        for item in new_requests:
            print(item.lor.user.id)
            details = {}
            print(StudentDetails.objects.filter(user=item.lor.user), item)
            lor_details = json.loads(serialize('json', Lor.objects.filter(id=item.lor.id)))[0]["fields"]
            user_details = Student.objects.values("id_num", "email", "name").get(id_num=item.lor.user.id_num)
            profile_details = json.loads(serialize('json', StudentDetails.objects.filter(user=item.lor.user)))[0][
                "fields"]
            details["student_details_general"] = user_details
            details["lor_details"] = lor_details
            details["student_details_profile"] = profile_details
            details["application_details"] = json.loads(serialize('json', FacultyListLor.objects.filter
            (faculty=self.request.user.psrn, application_status='CO', lor=item.lor.id)))[0]["fields"]
            result.append(details)
        return Response(result)


class GetStudentProfilePhoto(APIView):
    permission_classes = [
       IsFaculty
    ]

    def get(self, request, student_id):
        try:
            obj = StudentProfilePicture.objects.get(user=student_id)
            obj_image_url = obj.picture
            image_path = os.path.join(BASE_DIR, 'media', str(obj_image_url))
            last_dot = str(obj.picture).rfind('.')
            image_format = str(obj.picture)[last_dot + 1:len(str(obj.picture))]
            content_type = "image/" + image_format
            print(content_type, obj_image_url)
            with open(image_path, "rb") as image_file:
                base64string = base64.b64encode(image_file.read())
                return HttpResponse(base64string, content_type=content_type)
        except ObjectDoesNotExist or FileNotFoundError:
            return Response({'status': False})
