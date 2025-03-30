from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Message

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class MessageForm(forms.ModelForm):
    plaintext_message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': 'form-control',
            'placeholder': 'Type your message here...'
        }),
        help_text='Your message will be encrypted before sending.'
    )
    
    class Meta:
        model = Message
        fields = ['recipient']
        widgets = {
            'recipient': forms.Select(attrs={'class': 'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipient'].queryset = User.objects.exclude(public_key__isnull=True)
        self.fields['recipient'].help_text = 'Select a user to send the message to.'
