from django import forms
from django.forms import ModelForm
from .models import BabPengajaran, User, Feedback

# Form for Login
class UserForm(ModelForm):
    class Meta:
        model = User

        exclude = ['nik']

        widgets = {
            'username': forms.TextInput,
            'password': forms.PasswordInput
        }

# Form for Presensi
class BabPengajaranForm(ModelForm):
    class Meta:
        model = BabPengajaran
        fields = ['pertemuan_ke', 'tanggal', 'foto', 'status', 'materi', 'catatan_tambahan']

        status_Choices = [(0, 'Offline'),
                        (1, 'Online'),
                        (2, 'Libur')
                        ]
        widgets = {
            'pertemuan_ke': forms.NumberInput,
            'tanggal': forms.DateInput(attrs={'type': 'date'}),
            'foto': forms.FileInput,
            'status': forms.RadioSelect(choices=status_Choices),
            'materi': forms.NumberInput,
            'catatan_tambahan': forms.TextInput
        }

# Form for Feedback
class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback

        fields = ['feedback']

        widgets = {
            'feedback': forms.TextInput
        }