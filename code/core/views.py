from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Max, Min, Avg, Count
from .models import Course, CourseMember, Comment
from django.contrib.auth.models import User

# Dashboard page - Admin Overview
def dashboard(request):
    total_courses = Course.objects.count()
    total_users = User.objects.count()
    total_comments = Comment.objects.count()
    
    context = {
        'total_courses': total_courses,
        'total_users': total_users,
        'total_comments': total_comments,
    }
    return render(request, 'core/dashboard.html', context)

# Home page - Menampilkan semua course
def home(request):
    courses = Course.objects.select_related('teacher').annotate(
        member_count=Count('coursemember')
    ).all()
    
    # Course statistics
    stats = Course.objects.aggregate(
        total_courses=Count('id'),
        max_price=Max('price'),
        min_price=Min('price'),
        avg_price=Avg('price')
    )
    
    context = {
        'courses': courses,
        'stats': stats,
    }
    return render(request, 'core/home.html', context)

# [cite_start]1. Select Course with Teacher Data [cite: 344]
def allCourse(request):
    courses = Course.objects.select_related('teacher').all()
    result = []
    for c in courses:
        data = {
            'id': c.id,
            'name': c.name,
            'description': c.description,
            'price': c.price,
            'teacher': {
                'id': c.teacher.id,
                'username': c.teacher.username,
                'fullname': c.teacher.get_full_name() or c.teacher.username
            }
        }
        result.append(data)
    return JsonResponse(result, safe=False)

# [cite_start]2. Select User & His Courses (Sebagai Teacher) [cite: 375]
def userCourses(request):
    # Mengambil user pertama sebagai contoh
    user = User.objects.first() 
    courses = Course.objects.filter(teacher=user)
    
    course_list = []
    for c in courses:
        course_list.append({
            'id': c.id,
            'name': c.name,
            'price': c.price
        })
        
    result = {
        'user_id': user.id,
        'username': user.username,
        'courses_taught': course_list
    }
    return JsonResponse(result, safe=False)

# [cite_start]3. Course Stats (Aggregate) [cite: 403]
def courseStat(request):
    stats = Course.objects.aggregate(
        max_price=Max('price'),
        min_price=Min('price'),
        avg_price=Avg('price')
    )
    count = Course.objects.count()
    return JsonResponse({'total_course': count, 'stats': stats})

# [cite_start]4. Course with Member Count (Annotate) [cite: 418]
def courseMemberStat(request):
    # Filter course yg mengandung kata 'Belajar' (sesuai data csv)
    courses = Course.objects.filter(name__icontains='Belajar') \
                            .annotate(member_count=Count('coursemember'))
    
    data = []
    for c in courses:
        data.append({
            'name': c.name,
            'price': c.price,
            'jumlah_member': c.member_count
        })
        
    return JsonResponse({'data': data}, safe=False)