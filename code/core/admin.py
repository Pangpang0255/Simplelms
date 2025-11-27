from django.contrib import admin
from .models import Course, CourseMember, CourseContent, Comment, Completion

# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher', 'price', 'created_at']
    list_filter = ['teacher', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informasi Mata Kuliah', {
            'fields': ('name', 'description', 'price', 'teacher')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(CourseMember)
class CourseMemberAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'course_id', 'role', 'created_at']
    list_filter = ['role', 'created_at', 'course_id']
    search_fields = ['user_id__username', 'course_id__name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informasi Member', {
            'fields': ('user_id', 'course_id', 'role')
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(CourseContent)
class CourseContentAdmin(admin.ModelAdmin):
    list_display = ['name', 'course_id', 'parent_id', 'created_at']
    list_filter = ['course_id', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informasi Konten', {
            'fields': ('course_id', 'name', 'description', 'parent_id')
        }),
        ('Media', {
            'fields': ('video_url', 'file_attachment')
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'content_id', 'comment_preview', 'created_at']
    list_filter = ['created_at', 'content_id']
    search_fields = ['comment', 'user_id__username']
    readonly_fields = ['created_at', 'updated_at']
    
    def comment_preview(self, obj):
        return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment
    comment_preview.short_description = 'Preview Komentar'
    
    fieldsets = (
        ('Informasi Komentar', {
            'fields': ('user_id', 'content_id', 'comment')
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Completion)
class CompletionAdmin(admin.ModelAdmin):
    list_display = ['member_id', 'content_id', 'last_update']
    list_filter = ['last_update']
    search_fields = ['member_id__user_id__username', 'content_id__name']
    readonly_fields = ['last_update']
    
    fieldsets = (
        ('Informasi Completion', {
            'fields': ('member_id', 'content_id')
        }),
        ('Timestamp', {
            'fields': ('last_update',),
            'classes': ('collapse',)
        }),
    )

