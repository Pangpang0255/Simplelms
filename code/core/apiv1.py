from ninja import NinjaAPI, Schema
from pydantic import field_validator
import re
from .models import User, CourseMember, CourseContent, Comment, Course
from typing import List
import sys
import os

# Add parent directory to path to import api
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api import apiAuth

apiv1 = NinjaAPI()

@apiv1.get('/hello/')
def helloApi(request):
    return "Menyala abangkuh ..."

@apiv1.get('/calc/{nil1}/{opr}/{nil2}')
def calculator(request, nil1:int, opr:str, nil2:int):
    hasil = nil1 + nil2
    if opr == '-':
        hasil = nil1 - nil2
    elif opr == 'x':
        hasil = nil1 * nil2
    
    return {'nilai1': nil1, 'nilai2': nil2, 'operator': opr, 'hasil': hasil}

@apiv1.post('/hello-post/')
def helloPost(request):
    if 'nama' in request.POST:
        return f"Selamat menikmati ya {request.POST['nama']}"
    return "Selamat tinggal dan pergi lagi"

@apiv1.put('/users/{id}')
def userUpdate(request, id:int):
    return f"User dengan id {id} Nama aslinya adalah Herdiono kemudian diganti menjadi {request.body}"

@apiv1.delete('/users/{id}')
def userDelete(request, id:int):
    return f"Hapus user dengan id: {id}"

class Kalkulator(Schema):
    nil1: int
    nil2: int
    opr: str
    hasil: int = 0

    def calcHasil(self):
        hasil = self.nil1 + self.nil2
        if self.opr == '-':
            hasil = self.nil1 - self.nil2
        elif self.opr == 'x':
            hasil = self.nil1 * self.nil2

        return {'nilai1': self.nil1, 'nilai2': self.nil2,
                'operator': self.opr, 'hasil': self.hasil}

@apiv1.post('/calc/')
def postCalc(request, skim: Kalkulator):
    skim.hasil = skim.calcHasil()
    return skim

class Register(Schema):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str

class UserOut(Schema):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str

@apiv1.post('/register/', response=UserOut)
def register(request, data: Register):
    """
    - Endpoint untuk registrasi pengguna dengan validasi inputan:
    - username: minimal terdiri dari 5 karakter
    - password: minimal terdiri dari 8 karakter dan harus mengandung huruf dan angka
    """
    newUser = User.objects.create_user(username=data.username,
                                       password=data.password,
                                       email=data.email,
                                       first_name=data.first_name,
                                       last_name=data.last_name)

    return newUser

@field_validator('username')
def validate_username(cls, value):
    if len(value) < 5:
        raise ValueError("Username harus lebih dari 3 karakter")
    return value

@field_validator('password')
def validate_password(cls, value):
    if len(value) < 8:
        raise ValueError("Password harus lebih dari 8 karakter")

    pattern = r"^(?=.*[A-Za-z])(?=.*\d).+$"
    if not re.match(pattern, value):
        raise ValueError("Password harus mengandung huruf dan angka")
    return value


class UserSchema(Schema):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str

@apiv1.get('/users/', response=List[UserSchema])
def list_users(request):
    users = User.objects.all()
    return users

class CourseMemberOut(Schema):
    id: int
    course_name: str
    user_username: str
    role: str

class CommentIn(Schema):
    content_id: int
    comment: str

@apiv1.get('/mycourses/', auth=apiAuth, response=List[CourseMemberOut])
def getMyCourses(request):
    user_id = User.objects.get(pk=request.user.id)
    mycourses = CourseMember.objects.filter(user_id=user_id)\
        .select_related('course_id', 'user_id')
    return [
        CourseMemberOut(
            id=cm.id,
            course_name=cm.course_id.name,
            user_username=cm.user_id.username,
            role=cm.role
        ) for cm in mycourses
    ]

@apiv1.post('/course/{id}/enroll/', auth=apiAuth, response=CourseMemberOut)
def courseEnrollment(request, id: int):
    user_id = User.objects.get(pk=request.user.id)
    course = Course.objects.get(pk=id)
    enrollment = CourseMember.objects.create(user_id=user_id, course_id=course)
    return CourseMemberOut(
        id=enrollment.id,
        course_name=enrollment.course_id.name,
        user_username=enrollment.user_id.username,
        role=enrollment.role
    )

@apiv1.post('/komen/', auth=apiAuth)
def postComment(request, data: CommentIn):
    user_id = User.objects.get(pk=request.user.id)
    content_id = CourseContent.objects.filter(id=data.content_id).first()
    if not content_id:
        return {"status": "KONTEN TIDAK DITEMUKAN"}
    coursemember = CourseMember.objects.filter(user_id=user_id, course_id=content_id.course_id)
    if coursemember.exists():
        Comment.objects.create(comment=data.comment, user_id=user_id, content_id=content_id)
        return {"status": "berhasil"}
    else:
        return {"status": "berhasil "}