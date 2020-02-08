import base64
import json
import os

from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from users.permissions import *
from lor_tracker.serializers import *
from backend.settings import BASE_DIR


class GetAllRequests(APIView):
    permission_classes = [
        IsHoD
    ]
    
    # serializer_class = StudentProfileSerializer
    def get(self, request):
        result = []
        students = Student.objects.values("id_num", "email", "name").all()
        for item in students:
            details = {}
            lors = Lor.objects.values("id", "created_at").filter(user=item["id_num"])
            app_cnt = 0
            for lor_item in lors:
                list_lor = FacultyListLor.objects.filter(lor=lor_item["id"])
                app_cnt += list_lor.count()
            if app_cnt > 0:
                profile_details = json.loads(serialize('json', StudentDetails.objects.filter(user=item["id_num"])))[0][
                    "fields"]
                details["student_details_general"] = item
                details["student_details_profile"] = profile_details
                details["noOfRequests"] = app_cnt
                details["type"] = 'all'
                result.append(details)
        
        return Response(result)


class GetAcceptedEntriesHod(APIView):
    permission_classes = [
        IsHoD
    ]
    
    def get(self, request):
        result = []
        students = Student.objects.values("id_num", "email", "name").all()
        for item in students:
            details = {}
            lors = Lor.objects.values("id", "created_at").filter(user=item["id_num"])
            app_cnt = 0
            for lor_item in lors:
                list_lor = FacultyListLor.objects.filter(lor=lor_item["id"], application_status='AC')
                app_cnt += list_lor.count()
            if app_cnt > 0:
                profile_details = json.loads(serialize('json', StudentDetails.objects.filter(user=item["id_num"])))[0][
                    "fields"]
                details["student_details_general"] = item
                details["student_details_profile"] = profile_details
                details["noOfRequests"] = app_cnt
                details["type"] = 'AC'
                result.append(details)
        return Response(result)


class GetAllNewRequestsHod(APIView):
    permission_classes = [
        IsHoD
    ]
    
    # serializer_class = StudentProfileSerializer
    def get(self, request):
        result = []
        students = Student.objects.values("id_num", "email", "name").all()
        for item in students:
            details = {}
            lors = Lor.objects.values("id", "created_at").filter(user=item["id_num"])
            app_cnt = 0
            for lor_item in lors:
                list_lor = FacultyListLor.objects.filter(lor=lor_item["id"], application_status='AP')
                app_cnt += list_lor.count()
            if app_cnt > 0:
                profile_details = json.loads(serialize('json', StudentDetails.objects.filter(user=item["id_num"])))[0][
                    "fields"]
                details["student_details_general"] = item
                details["student_details_profile"] = profile_details
                details["noOfRequests"] = app_cnt
                details["type"] = 'AP'
                result.append(details)
        return Response(result)


class GetAllCompletedRequestsHod(APIView):
    permission_classes = [
        IsHoD
    ]
    
    def get(self, request):
        result = []
        students = Student.objects.values("id_num", "email", "name").all()
        for item in students:
            details = {}
            lors = Lor.objects.values("id", "created_at").filter(user=item["id_num"])
            app_cnt = 0
            for lor_item in lors:
                list_lor = FacultyListLor.objects.filter(lor=lor_item["id"], application_status='CO')
                app_cnt += list_lor.count()
            if app_cnt > 0:
                profile_details = json.loads(serialize('json', StudentDetails.objects.filter(user=item["id_num"])))[0][
                    "fields"]
                details["student_details_general"] = item
                details["student_details_profile"] = profile_details
                details["noOfRequests"] = app_cnt
                details["type"] = 'CO'
                result.append(details)
        return Response(result)


class GetHodHome(APIView):
    permission_classes = [
        IsHoD
    ]
    
    def get(self, request):
        result = {}
        new_requests = FacultyListLor.objects.filter(application_status='AP')
        accepted_requests = FacultyListLor.objects.filter(application_status='AC')
        completed_requests = FacultyListLor.objects.filter(application_status='CO')
        active_users = Session.objects.all()
        faculty = Faculty.objects.all()
        student = Student.objects.all()
        result["newRequests"] = len(new_requests)
        result["acceptedRequests"] = len(accepted_requests)
        result["completedRequests"] = len(completed_requests)
        result["facultyCnt"] = len(faculty)
        result["studentCnt"] = len(student)
        result["activeUserCnt"] = len(active_users)
        # result["activeUserContent"] = current_users_json
        return Response(result)


class GetAllStudents(APIView):
    permission_classes = [
        IsHoD
    ]
    
    def get(self, request):
        result = []
        new_requests = Student.objects.values("id_num", "email", "name").all()
        if not len(new_requests) == 0:
            for item in new_requests:
                details = {}
                try:
                    # json.loads(serialize('json', StudentDetails.objects.get(user=item["id"])))
                    student_details = StudentDetails.objects.values("phone", "graduation_status", "student_id",
                                                                    "full_name", "cgpa", 'degree').get(user=item["id_num"])
                    details["student_details_general"] = item
                    details["student_details_profile"] = student_details
                    result.append(details)
                except ObjectDoesNotExist as noProfile:
                    details["student_details_general"] = item
                    details["student_details_profile"] = {'dummy': 'done'}
                    result.append(details)
        return Response(result)


# class GetActiveUsers(APIView):
#     permission_classes = [
#         IsHoD
#     ]
#
# # serializer_class = StudentProfileSerializer def get(self, request): result = {} active_users =
# Session.objects.all() uid_list = [] for session in active_users: data = session.get_decoded() print(data.get(
# '_auth_user_id', None), str(self.request.user.id), data.get('_auth_user_id', None) == str(self.request.user.id)) if
# not data.get('_auth_user_id', None) == str(self.request.user.id): uid_list.append(data.get('_auth_user_id',
# None)) current_users = AppUser.objects.values("id", "email", "first_name", "last_name", "role").filter(
# id__in=uid_list) current_users_json = [] if not len(current_users) == 0: current_users_json = current_users result[
# "activeUserCnt"] = len(current_users) result["activeUserContent"] = current_users_json return Response(result)


class GetStudentProfilePhoto(APIView):
    permission_classes = [
        IsHoD
    ]
    required_groups = {
        'GET': ['hod'],
    }
    
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
        except ObjectDoesNotExist:
            return Response({'status': False})
