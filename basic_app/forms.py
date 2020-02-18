from django import forms
from django.contrib.auth.models import User
from .models import UserProfileInfo

#
class UserForm(forms.ModelForm):
    password = forms.CharField(label = "密碼",widget=forms.PasswordInput())
    last_name = forms.CharField(label = "名",required=True)
    first_name = forms.CharField(label = "姓",required=True)

    class Meta():
        model = User
        fields = ('username','email','password','first_name','last_name')


class UserProfileInfoForm(forms.ModelForm):
    show_out = forms.CharField(label = "簡單對外留言 YOUR MESSAGE（此訊息將公開給拾獲人）",required=False,widget=forms.Textarea)
    CHOICES = (('男性', '男性',), ('女性', '女性',),('不公開', '不公開',))
    gender = forms.ChoiceField(label = "性別", choices=CHOICES,required=True,initial='不公開')
    portfolio_site = forms.CharField(label = "手機號碼",required=True)
    class Meta():
        model = UserProfileInfo
        fields = ('gender','portfolio_site','FB_site','profile_pic','show_out')
class UserupdataForm(forms.ModelForm):
    password = forms.CharField(label = "密碼",widget=forms.PasswordInput(),required=False)
    last_name = forms.CharField(label = "名",required=False)
    first_name = forms.CharField(label = "姓",required=False)
    email = forms.EmailField(required=False)

    class Meta():
        model = User
        fields = ('email','password','first_name','last_name')
class UserupdataProfileInfoForm(forms.ModelForm):
    show_out = forms.CharField(label = "簡單對外留言 YOUR MESSAGE（此訊息將公開給拾獲人）",required=False,widget=forms.Textarea)
    CHOICES = (('男性', '男性',), ('女性', '女性',),('不公開', '不公開',))
    gender = forms.ChoiceField(label = "性別", choices=CHOICES)
    # Add any additional attributes you want
    portfolio_site = forms.CharField(label = "手機號碼",required=False)
    class Meta():
        model = UserProfileInfo
        fields = ('gender','portfolio_site','FB_site','profile_pic','show_out')
