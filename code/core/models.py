from django.db import models
from django.contrib.auth.models import User

# TABLE COURSE [cite: 20-38]
class Course(models.Model):
    # Diagram: teacher (int) -> Relasi ke User
    teacher = models.ForeignKey(User, verbose_name="pengajar", on_delete=models.RESTRICT)
    name = models.CharField("nama matkul", max_length=200) # Diagram: varchar(200) [cite: 30]
    description = models.TextField("deskripsi") # Diagram: text
    price = models.IntegerField("harga") # Diagram: int
    # Diagram: image varchar(200). Di Django best practice pakai ImageField (disimpan sebagai path string di DB)
    image = models.ImageField("gambar", upload_to='courses/', null=True, blank=True) 
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mata Kuliah"
        verbose_name_plural = "Mata Kuliah"

    def __str__(self):
        return self.name

# TABLE COURSE MEMBER [cite: 18-19]
class CourseMember(models.Model):
    ROLE_OPTIONS = [('std', "Siswa"), ('ast', "Asisten")] # [cite: 36]
    
    # Diagram: course_id (int)
    course_id = models.ForeignKey(Course, verbose_name="matkul", on_delete=models.RESTRICT)
    # Diagram: user_id (int)
    user_id = models.ForeignKey(User, verbose_name="siswa", on_delete=models.RESTRICT)
    role = models.CharField("peran", max_length=3, choices=ROLE_OPTIONS, default='std')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Subscriber Matkul"
        verbose_name_plural = "Subscriber Matkul"

    def __str__(self):
        return f"{self.user_id.username} in {self.course_id.name}"

# TABLE COURSE CONTENT [cite: 3-10]
class CourseContent(models.Model):
    # Diagram: course_id (int)
    course_id = models.ForeignKey(Course, verbose_name="matkul", on_delete=models.RESTRICT)
    name = models.CharField("judul konten", max_length=200)
    description = models.TextField("deskripsi", default='-')
    video_url = models.CharField('URL Video', max_length=200, null=True, blank=True)
    file_attachment = models.FileField("File", upload_to='files/', null=True, blank=True)
    # Diagram: parent_id (int)
    parent_id = models.ForeignKey("self", verbose_name="induk", on_delete=models.RESTRICT, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Konten Matkul"
        verbose_name_plural = "Konten Matkul"

    def __str__(self):
        return self.name

# TABLE COMMENT [cite: 42-56]
class Comment(models.Model):
    # Diagram menghubungkan content_id dan USER_ID (bukan member_id) 
    content_id = models.ForeignKey(CourseContent, verbose_name="konten", on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, verbose_name="pengguna", on_delete=models.CASCADE) 
    comment = models.TextField('komentar')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Komentar"
        verbose_name_plural = "Komentar"

    def __str__(self):
        return f"Comment by {self.user_id.username}"

# TABLE COMPLETION [cite: 11-17]
class Completion(models.Model):
    # Diagram menghubungkan member_id dan content_id [cite: 14-15]
    member_id = models.ForeignKey(CourseMember, on_delete=models.CASCADE)
    content_id = models.ForeignKey(CourseContent, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now=True) # Diagram: last_update datetime [cite: 16]

    class Meta:
        unique_together = ('member_id', 'content_id') # Agar satu member tidak double completion di satu konten