from django import forms
from captcha.fields import CaptchaField

class captchaTester(forms.Form):
    captcha=CaptchaField()