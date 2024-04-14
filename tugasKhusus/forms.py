from django import forms
from django.forms import ModelForm
from .models import BabPengajaran, Presensi


class BabPengajaranForm(ModelForm):

    def save(self, commit=True):
        instance = super().save(commit=False)  # Save the form data without saving the model

        # Access the uploaded file
        uploaded_file = self.cleaned_data['foto']
        instance.uploaded_file_name = uploaded_file.name  # Set the filename in the CharField

        if commit:
            instance.save()  # Save the model instance with the updated filename

        return instance

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

class PresensiSiswaForm(ModelForm):
    class Meta:
        model = Presensi
        fields = ['presensi']

        widgets = {
            'presensi': forms.NumberInput
        }