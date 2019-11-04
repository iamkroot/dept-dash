from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from research.models import ResearchScholar, ResearchWork, Publication, Project
from users.models import Faculty, Student

def create_groups_permissions():

    hod_group, created = Group.objects.get_or_create(name ='hod')
    faculty_group, created = Group.objects.get_or_create(name ='faculty')
    student_group, created = Group.objects.get_or_create(name ='student')
    faculty_group, created = Group.objects.get_or_create(name ='faculty')
    research_scholar_group, created = Group.objects.get_or_create(name ='researchScholar')
    
    add_student_permission = Permission.objects.get(name='Can add student')
    change_student_permission = Permission.objects.get(name='Can change student')
    view_student_permission = Permission.objects.get(name='Can view student')
    delete_student_permission = Permission.objects.get(name='Can delete student')

    hod_group.permissions.set([add_student_permission, change_student_permission, view_student_permission, delete_student_permission])

create_groups_permissions()