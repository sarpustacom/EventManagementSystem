from . import models
from django import forms

class EventForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"
            field.widget.attrs['placeholder'] = field.label

    class Meta:
        model = models.EventModel
        fields = ['title', 'description', 'date', 'time', 'location', 'coverphoto']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

class AttendeeForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"
            field.widget.attrs['placeholder'] = field.label

    class Meta:
        model = models.AttendeeModel
        fields = ['name', 'email', 'phone']