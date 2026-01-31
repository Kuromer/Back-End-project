from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('homepage/', homepage, name='home'),       
    path('dashboard/', dashboard, name='dashboard'), 
    path('add_course/', add_course, name='add_course'),
    path('edit_course/<int:course_id>/', edit_course, name='edit_course'),
    path('delete_course/<int:course_id>/', delete_course, name='delete_course'),
    path('', landing_page, name='landing_page'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)