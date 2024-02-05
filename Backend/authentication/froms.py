from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    user_bio = forms.CharField(label="Profile Bio", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description'}))

    class Meta:
          model = Profile
          fields = ('user_bio',) 
	    

