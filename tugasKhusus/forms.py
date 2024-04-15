from django import forms
from django.forms import ModelForm
from .models import BabPengajaran


class BabPengajaranForm(ModelForm):
    class Meta:
        model = BabPengajaran
        fields = ['pertemuan_ke', 'tanggal', 'foto', 'status', 'materi', 'catatan_tambahan']

        widgets = {
            'pertemuan_ke': forms.NumberInput,
            'tanggal': forms.DateInput(attrs={'type': 'date'}),
            'foto': forms.FileInput,
            'status': forms.NumberInput,
            'materi': forms.NumberInput,
            'catatan_tambahan': forms.TextInput
        }