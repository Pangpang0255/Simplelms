from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/courses/', views.allCourse, name='all_courses'),
    path('api/user-courses/', views.userCourses, name='user_courses'),
    path('api/course-stats/', views.courseStat, name='course_stats'),
    path('api/course-member-stats/', views.courseMemberStat, name='course_member_stats'),
]
