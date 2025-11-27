import os
import sys
import csv
import django

# Setup Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 3)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'simplelms.settings' # GANTI 'simplelms' dengan nama folder projectmu
django.setup()

from django.contrib.auth.models import User
from core.models import Course, CourseMember, CourseContent, Comment # GANTI 'core' dengan nama app kamu

print("=== Mulai Import ===")

# [cite_start]1. Import User [cite: 289]
print("Importing Users...")
with open(os.path.join(BASE_DIR, 'csv_data', 'user_data.csv')) as csvfile:
    reader = csv.DictReader(csvfile)
    for num, row in enumerate(reader):
        if not User.objects.filter(username=row['username']).exists():
            User.objects.create_user(
                username=row['username'],
                password=row['password'],
                email=row['email']
            )
            print(f"User {row['username']} created")

# [cite_start]2. Import Course [cite: 308]
print("\nImporting Courses...")
try:
    with open(os.path.join(BASE_DIR, 'csv_data', 'course-data.csv')) as csvfile:
        reader = csv.DictReader(csvfile)
        for num, row in enumerate(reader):
            # Random teacher dari semua user yang ada
            import random
            all_users = list(User.objects.all())
            teacher_obj = random.choice(all_users) if all_users else User.objects.first()
            
            if not Course.objects.filter(name=row['name']).exists():
                Course.objects.create(
                    name=row['name'],
                    description=row['description'],
                    price=int(row['price']),
                    teacher=teacher_obj
                )
                print(f"Course {row['name']} created with teacher {teacher_obj.username}")
except Exception as e:
    print(f"Error Course: {e}")

# [cite_start]3. Import Member [cite: 326]
print("\nImporting Members...")
try:
    with open(os.path.join(BASE_DIR, 'csv_data', 'member-data.csv')) as csvfile:
        reader = csv.DictReader(csvfile)
        for num, row in enumerate(reader):
            c_obj = Course.objects.get(id=int(row['course_id']))
            u_obj = User.objects.get(id=int(row['user_id']))
            
            if not CourseMember.objects.filter(course_id=c_obj, user_id=u_obj).exists():
                CourseMember.objects.create(
                    course_id=c_obj,
                    user_id=u_obj,
                    role=row['roles']
                )
                print(f"Member {u_obj.username} added to {c_obj.name}")
except Exception as e:
    print(f"Error Member: {e} (Pastikan ID course/user di CSV valid dengan database)")

# [cite_start]4. Import Course Content
print("\nImporting Course Contents...")
try:
    with open(os.path.join(BASE_DIR, 'csv_data', 'content-data.csv')) as csvfile:
        reader = csv.DictReader(csvfile)
        for num, row in enumerate(reader):
            c_obj = Course.objects.get(id=int(row['course_id']))
            
            # Handle parent_id (bisa kosong)
            parent_obj = None
            if row['parent_id'] and row['parent_id'].strip():
                try:
                    parent_obj = CourseContent.objects.get(id=int(row['parent_id']))
                except CourseContent.DoesNotExist:
                    pass
            
            # Cek apakah sudah ada
            existing = CourseContent.objects.filter(name=row['name'], course_id=c_obj).first()
            if not existing:
                content = CourseContent.objects.create(
                    course_id=c_obj,
                    name=row['name'],
                    description=row['description'],
                    video_url=row['video_url'],
                    parent_id=parent_obj
                )
                print(f"Content '{row['name']}' (ID: {content.id}) added to {c_obj.name}")
            else:
                print(f"Content '{row['name']}' already exists")
except Exception as e:
    print(f"Error Content: {e}")
    import traceback
    traceback.print_exc()

# [cite_start]5. Import Comments
print("\nImporting Comments...")
try:
    with open(os.path.join(BASE_DIR, 'csv_data', 'comment-data.csv')) as csvfile:
        reader = csv.DictReader(csvfile)
        for num, row in enumerate(reader):
            content_obj = CourseContent.objects.get(id=int(row['content_id']))
            user_obj = User.objects.get(id=int(row['user_id']))
            
            Comment.objects.create(
                content_id=content_obj,
                user_id=user_obj,
                comment=row['comment']
            )
            print(f"Comment by {user_obj.username} added to '{content_obj.name}'")
except Exception as e:
    print(f"Error Comment: {e}")

print("=== Selesai ===")