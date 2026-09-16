from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('consultation/', views.online_consultation_view, name='consultation'),
    path('provider/', views.provider_info_view, name='provider'),
    path('diseases/', views.diseases_view, name='diseases'),
    path('diseases/<slug:slug>/', views.disease_detail_view, name='disease_detail'),
    path('testimonials/', views.testimonials_view, name='testimonials'),
    path('testimonials/<slug:slug>/', views.testimonial_detail_view, name='testimonial_detail'),
    path('blogs/', views.blogs_view, name='blogs'),
    path('blogs/<slug:slug>/', views.blog_detail_view, name='blog_detail'),
    path('contact/', views.contact_view, name='contact'),
    path('contact/success/', views.contact_success_view, name='contact_success'),
    path('disclaimer/', views.disclaimer_view, name='disclaimer'),
]