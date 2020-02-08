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
from rest_framework import permissions, generics
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.settings import BASE_DIR
from backend.settings import EMAIL_HOST_USER
from users.permissions import *
from lor_tracker.serializers import *
from lor_tracker.validations.validate_lor_submission import validate_lor_submission, validate_edit_lor_submission

WITHDRAW_TEMPLATE = """
Dear {{faculty.first_name}} {{faculty.last_name}}:

The Letter of Recommendation request from {{student.full_name}}, has been withdrawn by the student.

Best Regards,
Head of the Department
Departments of Computer Science and Information Systems

For any query or inconvenience related to accessing the site please email to lor@hyderabad.bits-pilani.ac.in
"""
APPLICATION_TEMPLATE = """
Dear {{faculty.first_name}} {{faculty.last_name}}:

You got a new Letter of Recommendation request from {{student.full_name}}, it has to be filled by {{deadline}} if you accept it.
To accept the request please visit the department website

Thank You,

Best Regards,
Head of the Department
Departments of Computer Science and Information Systems

For any query or inconvenience related to accessing the site please email to lor@hyderabad.bits-pilani.ac.in
"""
EDITLOR_TEMPLATE = """
Dear {{faculty.first_name}} {{faculty.last_name}}:

The Letter of Recommendation request from {{student.full_name}} has been edited by the student.
Please make note of new details from the site before filling the Lor Application
Current Deadline: {{deadline}}

Thank You,

Best Regards,
Head of the Department
Departments of Computer Science and Information Systems

For any query or inconvenience related to accessing the site please email to lor@hyderabad.bits-pilani.ac.in
"""


# Edit my profile
class EditProfile(generics.GenericAPIView):
    permission_classes = [
        IsStudent
    ]
    
    serializer_class = CreateProfileSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            existing = StudentDetails.objects.get(user=self.request.user.id_num)
            serializer = self.get_serializer(existing, data=request.data)
            serializer.is_valid(raise_exception=True)
            student_details = serializer.save()
            return Response({
                "profile": StudentProfileSerializer(student_details, context=self.get_serializer_context()).data,
            })
        except ObjectDoesNotExist as notCreated:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            student_details = serializer.save()
            return Response({
                "profile": StudentProfileSerializer(student_details, context=self.get_serializer_context()).data,
            })


class UploadProfilePicture(generics.GenericAPIView):
    permission_classes = [
        IsStudent
    ]
    
    parser_class = (MultiPartParser, FormParser, FileUploadParser)
    
    serializer_class = ProfilePictureSerializer
    
    def post(self, request, *args, **kwargs):
        print({'here': request.data})
        
        try:
            existing = StudentProfilePicture.objects.get(user=self.request.user.id_num)
            print(os.path.join(BASE_DIR, 'media', existing.picture.name))
            os.remove(os.path.join(BASE_DIR, 'media', existing.picture.name))
            print({'here': request.data})
            serializer = self.get_serializer(existing, data=request.data)
            serializer.is_valid(raise_exception=True)
            profile_picture = serializer.save()
            return Response({
                "profile": GetPictureSerializer(profile_picture, context=self.get_serializer_context()).data,
            })
        except ObjectDoesNotExist as notCreated:
            print({'here': request.data})
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            profile_picture = serializer.save()
            return Response({
                "profile": GetPictureSerializer(profile_picture, context=self.get_serializer_context()).data,
            })


class GetMyProfilePicture(APIView):
    permission_classes = [
        IsStudent
    ]
    
    parser_class = (MultiPartParser, FormParser, FileUploadParser)
    serializer_class = GetPictureSerializer
    
    def get(self, request):
        try:
            entries = StudentProfilePicture.objects.get(user=self.request.user.id_num)
            return Response(GetPictureSerializer(entries).data)
        except ObjectDoesNotExist:
            return Response({'status': False})


# View profile
class GetMyProfile(APIView):
    permission_classes = [
        IsStudent
    ]
    
    serializer_class = StudentProfileSerializer
    
    def get(self, request):
        try:
            entries = StudentDetails.objects.get(user=self.request.user.id_num)
            return Response(StudentProfileSerializer(entries).data)
        except ObjectDoesNotExist:
            return Response({'status': False})


# Create an LOR Application
class CreateLor(generics.GenericAPIView):
    permission_classes = [
        IsStudent
    ]
    
    serializer_class = CreateLorRequestSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            existing = StudentDetails.objects.get(user=self.request.user.id_num)
            print("Data: ", request.data)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            lor_details = serializer.save()
            return Response({
                "lor": ViewSavedLor(lor_details, context=self.get_serializer_context()).data,
            })
        except ObjectDoesNotExist as notCreated:
            errors = {
                "profile": 'You have not created your profile yet, please create your profile before creating LOR'}
            raise ValidationError(errors)


class EditLor(generics.GenericAPIView):
    permission_classes = [
        IsStudent
    ]
    
    serializer_class = EditLorRequestSerializer
    
    def post(self, request, lor_id):
        try:
            # existing = StudentDetails.objects.get(user=self.request.user.id_num)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            lor_details = serializer.update(Lor.objects.get(id=lor_id), serializer.run_validation(data=request.data))
            applications = FacultyListLor.objects.filter(lor=lor_details.id)
            for item in applications:
                template = Template(EDITLOR_TEMPLATE)
                faculty_details = GetFacultyListSerializer(Faculty.objects.get(psrn=item.faculty.psrn)).data
                details = StudentDetails.objects.get(user=self.request.user.id_num)
                send_mail(
                    'Lor Updated: Student has changed the details of LOR ',
                    template.render(
                        context=Context(
                            {'faculty': faculty_details, 'student': details, 'deadline': lor_details.deadline})),
                    EMAIL_HOST_USER,
                    [faculty_details["email"]],
                    fail_silently=False,
                )
            return Response({
                "lor": ViewSavedLor(lor_details, context=self.get_serializer_context()).data,
            })
        except ObjectDoesNotExist as notCreated:
            errors = {
                "profile": 'You have not created your profile yet, please create your profile before creating LOR'}
            raise ValidationError(errors)


# Add Faculty Recipient for LOR
class AddFacultyForLOR(generics.GenericAPIView):
    permission_classes = [
        IsStudent
    ]
    
    serializer_class = AddFacultyToLorSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        validate_lor_submission(data=request.data)
        entries = []
        flag = 0
        creation_errors = {}
        for validated_data in request.data:
            selected_lor = Lor.objects.get(id=validated_data['lor_id'])
            if selected_lor.deadline.replace(tzinfo=None) <= datetime.now().replace(tzinfo=None):
                errors = {
                    "lor": 'Your LOR is expired, choose another one'}
                raise ValidationError(errors)
            else:
                check_exists = FacultyListLor.objects.filter(faculty=validated_data['faculty_id'],
                                                             lor=validated_data['lor_id']).count()
                if check_exists > 0:
                    flag = 1
                    creation_errors = {
                        'application': 'Lor already requested'
                    }
                else:
                    entry = FacultyListLor.objects.create(
                        lor_id=validated_data['lor_id'],
                        faculty_id=validated_data['faculty_id'],
                        courses_done=validated_data['courses_done'],
                        projects_done=validated_data['projects_done'],
                        thesis_done=validated_data['thesis_done'],
                        status=validated_data['status'],
                        others=validated_data['others'],
                        strengths=validated_data['strengths'],
                        comments=validated_data['comments'],
                    )
                    print(entry)
                    template = Template(APPLICATION_TEMPLATE)
                    faculty_details = Faculty.objects.get(psrn=validated_data['faculty_id'])
                    details = StudentDetails.objects.get(user=self.request.user.id_num)
                    lor = Lor.objects.get(id=validated_data['lor_id'])
                    dead_line = lor.deadline.replace(tzinfo=timezone.utc).astimezone(tz=None)
                    send_mail(
                        'New LOR Request: You got new Request with deadline on ' + str(dead_line),
                        template.render(
                            context=Context({'faculty': faculty_details, 'student': details, 'deadline': dead_line})),
                        EMAIL_HOST_USER,
                        [faculty_details.email],
                        fail_silently=False,
                    )
                    entries.append(entry)
        if flag:
            raise ValidationError(creation_errors)
        return Response({"success": True})


class EditSubmittedLorCourseDetails(generics.GenericAPIView):
    permission_classes = [
        IsStudent
    ]

    serializer_class = EditSubmittedLorDetailsSerializer
    
    def post(self, request, faculty, lor):
        serializer = self.get_serializer(data=request.data)
        validate_edit_lor_submission(data=request.data)
        selected_lor = Lor.objects.get(id=lor)
        if selected_lor.deadline.replace(tzinfo=None) <= datetime.now().replace(tzinfo=None):
            errors = {
                "lor": 'Your LOR is expired, choose another one'}
            raise ValidationError(errors)
        else:
            check_exists = FacultyListLor.objects.filter(faculty=faculty, lor=lor)
            if check_exists.count() > 0:
                data = request.data
                updated_details = FacultyListLor.objects.filter(lor_id=lor,
                                                                faculty_id=faculty).update(
                    courses_done=data['courses_done'],
                    projects_done=data['projects_done'],
                    thesis_done=data['thesis_done'],
                    status=data['status'],
                    others=data['others'])
                template = Template(EDITLOR_TEMPLATE)
                lor = Lor.objects.get(id=lor)
                dead_line = lor.deadline.replace(tzinfo=timezone.utc).astimezone(tz=None)
                faculty_details = Faculty.objects.get(psrn=faculty)
                details = StudentDetails.objects.get(user=self.request.user.id_num)
                send_mail(
                    'Lor Updated: Student has updated the Courses, Project details of Request',
                    template.render(
                        context=Context(
                            {'faculty': faculty_details, 'student': details, 'deadline': dead_line})),
                    EMAIL_HOST_USER,
                    [faculty_details.email],
                    fail_silently=False,
                )
            else:
                creation_errors = {
                    'application': 'Lor already requested'
                }
                ValidationError(creation_errors)
        return Response({"success": True})


# View Saved Lor
class GetMySavedLor(APIView):
    permission_classes = [
        IsStudent
    ]

    serializer_class = ViewSavedLor
    
    def get(self, request):
        update_entries = Lor.objects.filter(user=self.request.user.id_num, deadline__lte=datetime.now(timezone.utc)
                                            , expired=False)
        for entry in update_entries:
            new_entries = FacultyListLor.objects.filter(lor=entry["id"],
                                                        application_status__in=['AC', 'AP']).update(
                application_status='EX')
        update_entries = Lor.objects.filter(user=self.request.user.id, deadline__lte=datetime.now(timezone.utc)
                                            , expired=False).update(expired=True)
        entries = Lor.objects.filter(user=self.request.user.id, hidden=False)
        return Response(ViewSavedLor(entries, many=True).data)


class GetLorForApplication(APIView):
    permission_classes = [
        IsStudent
    ]

    serializer_class = ViewSavedLor
    
    def get(self, request):
        entries = Lor.objects.filter(user=self.request.user.id_num, deadline__gt=datetime.now(timezone.utc), hidden=False)
        return Response(ViewSavedLor(entries, many=True).data)


class DeleteLor(APIView):
    permission_classes = [
        IsStudent
    ]
   
    serializer_class = ViewSavedLor
    
    def get(self, request, lor_id):
        entries = FacultyListLor.objects.filter(lor=lor_id).count()
        if entries > 0:
            hide = Lor.objects.filter(id=lor_id).update(hidden=True)
        else:
            delete_lor = Lor.objects.get(id=lor_id).delete()
        return Response({'Success': True})


class GetAppliedLor(APIView):
    permission_classes = [
        IsStudent
    ]
    
    serializer_class = ViewAppliedFacultyListSerializer
    
    def get(self, request):
        update_entries = Lor.objects.filter(user=self.request.user.id_num, deadline__lte=datetime.now(timezone.utc),
                                            expired=False)
        # print(update_entries)
        for entry in update_entries:
            new_entries = FacultyListLor.objects.filter(lor_id=entry.id,
                                                        application_status__in=['AC', 'AP']).update(
                application_status='EX')
        update_entries = Lor.objects.filter(user=self.request.user.id_num, deadline__lte=datetime.now(timezone.utc)
                                            , expired=False).update(expired=True)
        entries = Lor.objects.filter(user=self.request.user.id_num)
        result = []
        for entry in entries:
            str_data = serialize('json', FacultyListLor.objects.filter(lor=entry.id_num))
            data = json.loads(str_data)
            for item in data:
                print(json.loads(serialize('json', Lor.objects.filter(id=item["fields"]["lor"])))[0][
                          "fields"])
                item["fields"]["lor"] = ViewSavedLor(Lor.objects.get(id=item["fields"]["lor"])).data
                item["fields"]["faculty"] = Faculty.objects.values("psrn", "email", "name").filter(psrn=item["fields"]["faculty"])[0]
                result.append(item["fields"])
        return Response(result)


class WithdrawApplications(APIView):
    permission_classes = [
        IsStudent
    ]

    serializer_class = ViewAppliedFacultyListSerializer
    
    def get(self, request, lor, faculty):
        template = Template(WITHDRAW_TEMPLATE)
        faculty_details = Faculty.objects.get(psrn=faculty)
        details = StudentDetails.objects.get(user=self.request.user.id_num)
        try:
            check = FacultyListLor.objects.get(lor_id=lor, faculty_id=faculty)
            if check.application_status == 'AC' or check.application_status == 'AP':
                FacultyListLor.objects.get(lor=lor, faculty=faculty).delete()
                send_mail(
                    'Request Withdrawn: Lor Request has been Withdrawn by the student',
                    template.render(context=Context({'faculty': faculty_details, 'student': details})),
                    EMAIL_HOST_USER,
                    [faculty_details.email],
                    fail_silently=False,
                )
                return Response('Application Withdrawn')
            else:
                raise ValidationError({'error_delete': 'You cannot withdraw application at this stage'})
        except ObjectDoesNotExist as notCreated:
            return Response('Please wait while the photo is deleting')


# List of Universities in database
class GetUnivList(APIView):
    permission_classes = [
        IsStudent
    ]
    serializer_class = GetUnivListSerializer
    
    def get(self, request):
        entries = Lor.objects.order_by('university_name').values('university_name').distinct()
        print('University: ', entries)
        entries = list(entries)
        print('UniversityList: ', entries)
        return Response(entries)


# Get Faculty list
class GetFacultyList(APIView):
    permission_classes = [
        IsStudent
    ]

    serializer_class = GetFacultyListSerializer
    
    def get(self, request):
        entries = Faculty.objects.all()
        print(entries)
        return Response(GetFacultyListSerializer(entries, many=True).data)


class ViewProfilePhoto(APIView):
    # permission_classes = (permissions.AllowAny,)
    permission_classes = [
        IsStudent
    ]

    def get(self, request):
        try:
            obj = StudentProfilePicture.objects.get(user=self.request.user.id_num)
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


