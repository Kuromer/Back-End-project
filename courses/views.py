from django.shortcuts import render , redirect
from django.contrib.auth import login , logout , authenticate
from django.contrib.auth.models import User
from .models import StudentProfile , Course
from django.contrib.auth.decorators import login_required , user_passes_test
from .forms import CourseForm
# Create your views here.
def signup(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        Email = request.POST.get('email')
        Age = request.POST.get('age')
        Phone = request.POST.get('phone_number')
        Parent_phone = request.POST.get('parent_number')
        if User.objects.filter(username = user_name).exists():
            return render(request , 'signup2.html' , {'error' : 'Username already exists'})
        user = User.objects.create_user(username = user_name , password = pass_word , email = Email)
        student_profile = StudentProfile.objects.create(user = user , age = Age , phone = Phone , parent_phone = Parent_phone)
        login(request , user)
        return redirect('login')
    return render(request , 'signup2.html')

def login_view(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        user = authenticate(request , username = user_name , password = pass_word)
        if user is not None:
            login(request , user)
            return redirect('homepage')
        else:
            return render(request , 'index.html' , {'error' : 'Invalid credentials'})
    return render(request , 'index.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def is_teacher(user):
    return user.groups.filter(name='Teacher').exists()

@login_required
def homepage(request):
    course = Course.objects.all()
    return render(request , 'homepage.html' , {'course' : course})

def landing_page(request):
    return render(request , 'landing.html')

@user_passes_test(is_teacher)
@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST , request.FILES)
        if form.is_valid():
            course = form.save(commit = False)
            course.teacher = request.user
            course.save()
            return redirect('dashboard')
    else:
        form = CourseForm()
    return render(request , 'course_form.html' , {'form' : form})

@user_passes_test(is_teacher)
@login_required
def edit_course(request , course_id):
    course = Course.objects.get(Course,id = course_id)
    if course.teacher != request.user:
        return redirect('homepage')

    if request.method == 'POST':
        form = CourseForm(request.POST , request.FILES , instance = course)
        if form.is_valid():
            course = form.save(commit = False)
            course.teacher = request.user
            course.save()
            return redirect('dashboard')
    else:
        form = CourseForm(instance = course)
    return render(request , 'course_form.html' , {'form' : form})

@user_passes_test(is_teacher)
@login_required
def delete_course(request , course_id):
    course = Course.objects.get(Course,id = course_id)
    if course.teacher != request.user:
        return redirect('homepage')
    else:
        course.delete()
    return redirect('dashboard')

@user_passes_test(is_teacher)
@login_required
def dashboard(request):
    courses = Course.objects.filter(teacher=request.user)
    return render(request, 'dashboard.html', {'courses': courses})
