from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import StudentProfile, Course
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CourseForm

# 1. دالة التحقق (وحدناها لتعتمد على is_staff زي الـ HTML)
def is_teacher(user):
    return user.is_staff

# ---------------------------------------------------

def signup(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        Email = request.POST.get('email')
        Age = request.POST.get('age')
        Phone = request.POST.get('phone_number')
        Parent_phone = request.POST.get('parent_number')

        if User.objects.filter(username=user_name).exists():
            return render(request, 'signup2.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=user_name, password=pass_word, email=Email)

        # تصحيح: استخدام الأسماء الصحيحة للأعمدة
        StudentProfile.objects.create(user=user, age=Age, phone=Phone, parent_phone=Parent_phone)

        login(request, user)
        # بعد التسجيل بنوديه الصفحة الرئيسية مش صفحة الدخول تاني
        return redirect('home')

    return render(request, 'signup2.html')

def login_view(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        user = authenticate(request, username=user_name, password=pass_word)
        if user is not None:
            login(request, user)
            return redirect('home') # تأكد إن اسم الرابط في urls.py هو 'home'
        else:
            return render(request, 'index.html', {'error': 'Invalid credentials'})
    return render(request, 'index.html') # تأكد من اسم ملف الـ HTML

def logout_view(request):
    logout(request)
    return redirect('login')

# ---------------------------------------------------

def homepage(request):
    all_courses = Course.objects.all()
    # التصحيح: بعتناها باسم 'courses' (جمع) عشان تتوافق مع الـ HTML
    is_in_teacher_group = False
    if request.user.is_authenticated:
        is_in_teacher_group = request.user.groups.filter(name='Teacher').exists()
    return render(request, 'homepage.html', {'courses': all_courses , 'is_teacher':is_in_teacher_group})

def landing_page(request):
    return render(request, 'landing.html')

# ---------------------------------------------------
# دوال المدرسين (Dashboard)

@user_passes_test(is_teacher, login_url='home')
@login_required
def dashboard(request):
    courses = Course.objects.filter(teacher=request.user)
    return render(request, 'dashboard.html', {'courses': courses})

@user_passes_test(is_teacher, login_url='home')
@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            return redirect('dashboard')
    else:
        form = CourseForm()
    return render(request, 'course_form.html', {'form': form, 'title': 'Add New Course'})

@user_passes_test(is_teacher, login_url='home')
@login_required
def edit_course(request, course_id):
    # التصحيح: استخدام get_object_or_404 بدلاً من Syntax الخطأ القديم
    course = get_object_or_404(Course, id=course_id)

    # حماية: المدرس صاحب الكورس بس هو اللي يعدل
    if course.teacher != request.user:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CourseForm(instance=course)
    return render(request, 'course_form.html', {'form': form, 'title': 'Edit Course'})

@user_passes_test(is_teacher, login_url='home')
@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if course.teacher == request.user:
        course.delete()

    return redirect('dashboard')