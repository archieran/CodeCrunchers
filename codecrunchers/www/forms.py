from django.forms import ModelForm
from www.models import Profile
from django import forms

class ProfileForm(ModelForm):
    
    class Meta:
        model = Profile
        fields = ['user_type','user_avatar']
        widgets = {
            #'user_type': TextInput(attrs={'class': 'form-control'}),
            #'user_avatar': FileField(attrs={'class': "form-control"}),
            }