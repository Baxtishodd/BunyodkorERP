from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','email',)


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'birthday', 'profile_picture', 'job_role', 'address', 'phone', 'mobile', 'website', 'whatsapp', 'telegram']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'profile_picture': forms.FileInput(),
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ism'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Familiya'}))


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Qabul qiladi 150 belgilar yoki kamroq. Harflar, raqamlar, va faqat @/./+/-/_ belgialar. </small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Parol'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = ('<ul class="form-text text-muted small">'
                                              '<li>Sizning parol ma\'lumotlaringiz bilan bir hil bo\'lmasin!</li>'
                                                     '<li>Sizning parol 8 belgidan kam bo\'lmasin!</li>'
                                              '<li>Sizning parol juda ham oddiy bo\'lmasligi lozim!</li>'
                                              '<li>Sizning parol faqat raqamlardan tashkil topmasligi lozim!</li></ul>')

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Parol takroran'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Tastiqlash uchun. Parolni takroran yozing. </small></span>'
