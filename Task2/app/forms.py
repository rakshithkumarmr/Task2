from django import forms
from simplecaptcha import captcha
from simplecaptcha.fields import  CaptchaField
import re
from .models import ArticleModel

@captcha
class RegistrationForm(forms.Form):
    def clean_username(self):
        un = self.cleaned_data["username"]
        res = re.match("^[A-Za-z]*$",un)
        if res:
            return un
        else:
            raise forms.ValidationError("Username must contain characters only")
    def clean_password(self):
        pa = self.cleaned_data["password"]
        res = re.match("^[A-Za-z0-9 ]*$", pa)
        if res:
            return pa
        else:
            raise forms.ValidationError("Password must contain characters and numbers only")

    username = forms.CharField(max_length=20)
    password = forms.CharField(min_length=8,max_length=20,widget=forms.PasswordInput)
    confirm_password = forms.CharField(min_length=8,max_length=20,widget=forms.PasswordInput)
    captcha = CaptchaField()

class ArticleForm(forms.ModelForm):
    class Meta:
        model = ArticleModel
        fields = ['topic_name','image','description','article_type']