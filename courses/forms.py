from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'price', 'image', 'grade', 'tag']
        
        widgets = {
            'image': forms.FileInput(attrs={'class': 'input-field', 'placeholder': 'Course Image'}),
            'title': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Course Name'}),
            'description': forms.Textarea(attrs={'class': 'input-field', 'placeholder': 'Course Description', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'input-field', 'placeholder': 'Course Price'}),
            'grade': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Course Grade'}),
            'tag': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Course Tag'}),
        }