from django.db import models
from django.utils.text import slugify

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=150)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{name} - {self.subject} ({self.submitted_at.strftime('%Y-%m-%d %H:%M')})"


class ConsultationRequest(models.Model):
    # ① About You
    full_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    # ② Main Concern
    main_complaint = models.TextField(help_text="Primary health concern or symptom")
    duration = models.CharField(max_length=100, help_text="How long have you had this?")
    severity = models.CharField(max_length=50, help_text="Mild, Moderate, Severe, etc.")
    modalities = models.TextField(help_text="What makes it better or worse?")

    # ③ Medical History
    past_conditions = models.TextField(blank=True, null=True, help_text="Past illnesses or surgeries")
    allergies = models.TextField(blank=True, null=True)
    family_history = models.TextField(blank=True, null=True, help_text="Relevant family medical history")

    # ④ Current Treatment
    current_medications = models.TextField(blank=True, null=True)
    previous_treatments = models.TextField(blank=True, null=True, help_text="What have you tried so far?")

    # ⑤ Tell Me More (Constitutional & Lifestyle)
    sleep_appetite_emotions = models.TextField(help_text="Sleep patterns, appetite, thirst, thermal reactions, emotional state, and lifestyle")

    # Metadata
    date_submitted = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return f"Consultation: {self.full_name} - {self.main_complaint[:30]}"


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    author = models.CharField(max_length=100, default="Dr. Mani")
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    patient_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=200, blank=True, help_text="Unique URL path (auto-filled)")
    condition_treated = models.CharField(max_length=150, help_text="e.g., Chronic Sinusitis, Joint Pain")
    summary = models.TextField(help_text="Brief description for the flash card grid", blank=True, null=True)
    detailed_description = models.TextField(help_text="Full patient story for the detail page", blank=True, null=True)
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    review_text = models.TextField(help_text="Legacy review field (optional)")
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)
    date_posted = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.patient_name)
            slug = base_slug
            counter = 1
            while Testimonial.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient_name} - {self.condition_treated}"


class Disease(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, help_text="Unique URL path (auto-filled or manual)")
    category = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Respiratory, Musculoskeletal, Skin")
    summary = models.TextField(help_text="Brief overview of the condition")
    detailed_description = models.TextField(help_text="Comprehensive description, homeopathic approach, and key characteristics")
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='diseases/', blank=True, null=True)

    def __str__(self):
        return self.name