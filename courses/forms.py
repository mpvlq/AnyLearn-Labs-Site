from django import forms


class ContactForm(forms.Form):
    """Contact form with validation"""
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Twoje imię',
            'class': 'form-field',
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Twój email',
            'class': 'form-field',
        })
    )
    message = forms.CharField(
        max_length=2000,
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': 'Wiadomość',
            'class': 'form-field',
            'rows': 4,
            'style': 'resize: vertical; font-family: \'Lora\', Georgia, serif; height: auto;'
        })
    )


class NewsletterForm(forms.Form):
    """Newsletter subscription form with email validation"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Twój email',
            'class': 'form-input',
        })
    )
