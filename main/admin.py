from django.contrib import admin
from .models import BlogPost, Testimonial, ContactSubmission, ConsultationRequest, Disease

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at')
    search_fields = ('name', 'email', 'subject')
    
#registering the disease in admin
@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'date_added')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'category', 'summary')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'condition_treated', 'rating', 'date_posted')
    list_filter = ('rating', 'date_posted')
    search_fields = ('patient_name', 'condition_treated', 'review_text')

@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'main_complaint', 'date_submitted', 'is_reviewed')
    list_filter = ('is_reviewed', 'date_submitted')
    search_fields = ('full_name', 'email', 'main_complaint')