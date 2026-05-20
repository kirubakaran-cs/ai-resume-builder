from django import forms
from .models import Resume


class ResumeForm(forms.ModelForm):
    """
    Auto-generates form fields from the Resume model.
    We use 'fields' to control which fields appear and in what order.
    """
    class Meta:
        model = Resume
        exclude = ['user', 'summary', 'created_at', 'updated_at']
        widgets = {
            # Textarea widgets for multi-line fields
            'experience': forms.Textarea(attrs={'rows': 6, 'placeholder':
                'Software Engineer | Google | 2021-2024 | Built scalable microservices\n'
                'Intern | Startup | 2020-2021 | Developed REST APIs'}),
            'education': forms.Textarea(attrs={'rows': 4, 'placeholder':
                'B.Tech Computer Science | MIT | 2020\n'
                'HSC | City School | 2016'}),
            'skills': forms.Textarea(attrs={'rows': 3, 'placeholder':
                'Python, Django, PostgreSQL, REST APIs, Git, Docker'}),
            'projects': forms.Textarea(attrs={'rows': 5, 'placeholder':
                'Portfolio Website | Personal site built with Django | Python, Django, Bootstrap\n'
                'Chat App | Real-time messaging app | WebSockets, Redis'}),
            'certifications': forms.Textarea(attrs={'rows': 3, 'placeholder':
                'AWS Cloud Practitioner | 2023\n'
                'Google Data Analytics | 2022'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap class and placeholders to simple text fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['linkedin'].required = False
        self.fields['github'].required = False
        self.fields['projects'].required = False
        self.fields['certifications'].required = False