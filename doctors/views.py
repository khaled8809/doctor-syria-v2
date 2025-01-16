from django.shortcuts import render
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from .models import Doctor, Review, BlogPost, Specialty, Area

def search_doctors(request):
    query = request.GET.get('q', '')
    specialty = request.GET.get('specialty', '')
    area = request.GET.get('area', '')
    
    doctors = Doctor.objects.filter(is_available=True)
    
    if query:
        doctors = doctors.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(specialty__name__icontains=query)
        )
    
    if specialty:
        doctors = doctors.filter(specialty__name=specialty)
    
    if area:
        doctors = doctors.filter(area__name=area)
    
    # تحميل التخصصات والمناطق للفلترة
    specialties = Specialty.objects.all()
    areas = Area.objects.all()
    
    # تحميل التقييمات الأخيرة
    recent_reviews = Review.objects.select_related('doctor', 'patient')[:5]
    
    # تحميل المقالات الأخيرة
    recent_posts = BlogPost.objects.select_related('author')[:3]
    
    # إعداد التصنيف
    paginator = Paginator(doctors, 10)  # 10 أطباء في كل صفحة
    page = request.GET.get('page')
    doctors = paginator.get_page(page)
    
    context = {
        'doctors': doctors,
        'specialties': specialties,
        'areas': areas,
        'recent_reviews': recent_reviews,
        'recent_posts': recent_posts,
        'query': query,
        'selected_specialty': specialty,
        'selected_area': area,
    }
    
    return render(request, 'doctors/search.html', context)

def doctor_profile(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    reviews = Review.objects.filter(doctor=doctor).select_related('patient')
    
    # حساب متوسط التقييم
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    context = {
        'doctor': doctor,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
    }
    
    return render(request, 'doctors/profile.html', context)

def blog_list(request):
    category = request.GET.get('category', '')
    posts = BlogPost.objects.select_related('author')
    
    if category:
        posts = posts.filter(category=category)
    
    paginator = Paginator(posts, 6)  # 6 مقالات في كل صفحة
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'posts': posts,
        'selected_category': category,
        'categories': BlogPost.CATEGORIES,
    }
    
    return render(request, 'doctors/blog.html', context)
