from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
# SuperUserInformation
# User: Jose
# Email: training@pieriandata.com
# Password: testpassword

# Create your models here.


class UserProfileInfo(models.Model):

    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="電話格式應該要像: '+999999999或0912345678'.")
    # Add any additional attributes you want
    portfolio_site = models.CharField("手機號碼",validators=[phone_regex], max_length=17, blank=False)
    FB_site = models.CharField("FACEBOOK MESSENGER，例如https://m.me/XXXX，僅需輸入XXX部分",max_length=225, blank=True)
    # pip install pillow to use this!
    # Optional: pip install pillow --global-option="build_ext" --global-option="--disable-jpeg"
    profile_pic = models.ImageField(
        "個人圖片", upload_to='basic_app/profile_pics', blank=True)
    show_out = models.CharField("簡單對外留言 YOUR MESSAGE（此訊息將公開給拾獲人）", max_length=300,blank=True)
    gender = models.CharField("性別",max_length=10)
    show = models.IntegerField()
    item_show = models.CharField(max_length=300)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username