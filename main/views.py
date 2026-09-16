from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from .forms import ContactForm
from .models import BlogPost, Testimonial, ConsultationRequest, Disease
from .models import Testimonial

def home_view(request):
    # Fetch up to 3 featured conditions for the knowledge base preview
    featured_diseases = Disease.objects.all()[:3]
    
    context = {
        'featured_diseases': featured_diseases,
    }
    return render(request, 'main/home.html', context) #new

def online_consultation_view(request):
    if request.method == 'POST':
        # 1. Save the consultation request to the database
        ConsultationRequest.objects.create(
            full_name=request.POST.get('full_name'),
            age=request.POST.get('age') or None,
            gender=request.POST.get('gender'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            main_complaint=request.POST.get('main_complaint'),
            duration=request.POST.get('duration'),
            severity=request.POST.get('severity'),
            modalities=request.POST.get('modalities'),
            past_conditions=request.POST.get('past_conditions'),
            allergies=request.POST.get('allergies'),
            family_history=request.POST.get('family_history'),
            current_medications=request.POST.get('current_medications'),
            previous_treatments=request.POST.get('previous_treatments'),
            sleep_appetite_emotions=request.POST.get('sleep_appetite_emotions')
        )

        patient_name = request.POST.get('full_name')
        patient_email = request.POST.get('email')
        main_complaint = request.POST.get('main_complaint')

        # 2. Email notification to Dr. Mani
        admin_subject = f"New Consultation Request: {patient_name}"
        admin_message = (
            f"A new online consultation intake has been submitted.\n\n"
            f"Patient Name: {patient_name}\n"
            f"Email: {patient_email}\n"
            f"Phone: {request.POST.get('phone')}\n"
            f"Main Complaint: {main_complaint}\n\n"
            f"Log into the Django Admin panel to view the complete 5-part clinical case history."
        )
        send_mail(
            admin_subject,
            admin_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.CLINIC_NOTIFICATION_EMAIL],
            fail_silently=False,
        )

        # 3. Confirmation email to the patient
        patient_subject = "Consultation Request Received - Homoeocare by Dr. Mani"
        patient_message = (
            f"Dear {patient_name},\n\n"
            f"Thank you for submitting your online consultation request to Homoeocare by Dr. Mani. "
            f"We have received your case details regarding '{main_complaint}'.\n\n"
            f"Dr. Mani will carefully review your submission and contact you shortly to discuss "
            f"your treatment plan and schedule your consultation session.\n\n"
            f"Warm regards,\n"
            f"Homoeocare by Dr. Mani"
        )
        send_mail(
            patient_subject,
            patient_message,
            settings.DEFAULT_FROM_EMAIL,
            [patient_email],
            fail_silently=False,
        )

        return redirect('contact_success')
        
    return render(request, 'main/consultation.html')

def provider_info_view(request):
    return render(request, 'main/provider.html')

def provider_view(request):
    return render(request, 'main/provider.html') #provider image render

def diseases_view(request):
    query = request.GET.get('q', '')
    if query:
        diseases = Disease.objects.filter(
            Q(name__icontains=query) | Q(category__icontains=query) | Q(summary__icontains=query)
        ).order_by('name')
    else:
        diseases = Disease.objects.all().order_by('name')
        
    return render(request, 'main/diseases.html', {'diseases': diseases, 'query': query})

def disease_detail_view(request, slug):
    disease = get_object_or_404(Disease, slug=slug)
    return render(request, 'main/disease_detail.html', {'disease': disease})


def testimonials_view(request):
    testimonials = Testimonial.objects.all().order_by('-date_posted')
    return render(request, 'main/testimonials.html', {'testimonials': testimonials})

def testimonial_detail_view(request, slug):
    testimonial = get_object_or_404(Testimonial, slug=slug)
    return render(request, 'main/testimonial_detail.html', {'testimonial': testimonial})

def blogs_view(request):
    # Fetch only published blog posts, newest first
    posts = BlogPost.objects.filter(is_published=True).order_by('-published_date')
    return render(request, 'main/blogs.html', {'posts': posts})

def blog_detail_view(request, slug):
    # Fetch the specific blog post or return a 404 page if it doesn't exist
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    return render(request, 'main/blog_detail.html', {'post': post})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_success')
    else:
        form = ContactForm()
    
    return render(request, 'main/contact.html', {'form': form})

def contact_success_view(request):
    return render(request, 'main/contact_success.html')

def disclaimer_view(request):
    return render(request, 'main/disclaimer.html') #disclaimer