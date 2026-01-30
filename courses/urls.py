from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('homepage/', homepage, name='homepage'),
    path('dashboard/', dashboard, name='dashboard'),
    path('add_course/', add_course, name='add_course'),
    path('edit_course/<int:course_id>/', edit_course, name='edit_course'),
    path('delete_course/<int:course_id>/', delete_course, name='delete_course'),
    path('',landing_page, name='landing_page'),
]
