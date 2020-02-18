from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm, UserupdataForm, UserupdataProfileInfoForm
from .models import UserProfileInfo
from .models import User
from django.views.decorators.gzip import gzip_page

# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import smtplib
from email.mime.text import MIMEText

# Create your views here.

@gzip_page
def index(request):
    return render(request, 'basic_app/index.html')


@login_required
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/basic_app/user_login/'
    return HttpResponse("You are logged in. Nice!")


@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))


def register(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user
            profile.show = 0
            profile.item_show = '在此輸入物品說明'
            profile.FB_site = "https://m.me/" + profile.FB_site
            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']
            # Now save model

            gmail_user = 'bolo.ncku@gmail.com'
            gmail_password = 'bolosystem'  # your gmail password
            content_1 = """<!DOCTYPE html>
                            <html>
                            <head>
                                <title></title>
                                <link rel="stylesheet" type="text/css" href="main.css" > 
                                <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/slick-carousel@1.8.1/slick/slick.css"/>
                            </head>
                            <body>
                                <div style="margin:0 auto;"> 
                                    <div style="margin:0 auto;"> 
                                    <img src="https://www.boloncku.tk/media/mail_code/img/logo.png" style="width:200px; margin:0 auto; display:block;"> 
                                    </div> <!--header--> 
                                    <div style="width: 450px; margin:0 auto"> 
                                    <h2 style="margin:">""" + user.first_name + user.last_name + """ 您好，您已成功註冊Bolo 遺失物協尋平台</h2><br /> 
                                    <p style="margin:0">歡迎使用Bolo 遺失物協尋服務，您可以自由下載我們所提供的Qrcode 聯絡條碼，張貼在您的物品上，並且透過鎖頭控制自行決定是否公開聯絡資訊 ^_^</p> 
                                    
                                        <p style="margin:0;color:red"></p>  
                                        <hr>
                                        <div style="font-size:14px;">
                                        <p>注意事項：</p>
                                        <p style="margin:10px 0;">若有任何問題，歡迎透過Email詢問我們，謝謝！</p>
                                        </div>
                                    </div> <!--content-->
                                    <div style="width:550px; background-color:#eeeeee; padding:5px 0; color:#909090; margin:25px auto 0;">
                                    <p style="text-align: center; font-size:10px;">Bolo 遺失物協尋平台 © 2019 研究生好窮有限公司/成大工設所<br />本信由系統自動發送，如需服務請洽bolo.ncku@gmail.com</p>
                                    </div> <!--footer-->
                                </div>

                            </body>
                            </html>"""
            msg = MIMEText(content_1, _subtype='html')
            msg['Subject'] = '感謝您註冊bolo遺失物協尋平台'
            msg['From'] = gmail_user
            msg['To'] = user.email
            content_2 = '''<!DOCTYPE html>
                            <html>
                            <head>
                                <title></title>
                                <link rel="stylesheet" type="text/css" href="main.css" > 
                                <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/slick-carousel@1.8.1/slick/slick.css"/>
                            </head>
                            <body>
                                <div style="margin:0 auto;"> 
                                    <div style="margin:0 auto;"> 
                                    <img src="img/logo.png" style="width:200px; margin:0 auto; display:block;"> 
                                    </div> <!--header--> 
                                    <div style="width: 450px; margin:0 auto"> 
                                    <h2 style="margin:">Bolo遺失物平台收到新的會員註冊</h2><br /> 
                                    <p style="margin:0">以下是''' + user.first_name + user.last_name + '''的會員資訊</p> 
                                        <div style="margin: 25px 0">
                                        <ul style="color:#000;">
                                        <li style="margin:5px 0;">會員信箱 : ''' + user.email + '''</li>
                                        <li style="margin:5px 0;">會員電話 : '''+user.userprofileinfo.portfolio_site + '''</li>
                                        </ul>
                                    </div>
                                        <p style="margin:0;color:red"></p>  
                                        <hr>
                                        <div style="font-size:14px;">
                                        <p>注意事項：</p>
                                        <p style="margin:10px 0;">若有任何問題，歡迎透過Email詢問我們，謝謝！</p>
                                        </div>
                                    </div> <!--content-->
                                    <div style="width:550px; background-color:#eeeeee; padding:5px 0; color:#909090; margin:25px auto 0;">
                                    <p style="text-align: center; font-size:10px;">Bolo 遺失物協尋平台 © 2019 研究生好窮有限公司/成大工設所<br />本信由系統自動發送，如需服務請洽bolo.ncku@gmail.com</p>
                                    </div> <!--footer-->
                                </div>

                            </body>
                            </html>'''

            msg_me = MIMEText(content_2, _subtype='html')
            msg_me['Subject'] = user.first_name + \
                user.last_name+'成功註冊Bolo遺失物平台'
            msg_me['From'] = gmail_user
            msg_me['To'] = gmail_user

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.send_message(msg)
            server.quit()

            print('Email sent!')
            profile.save()
            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors, profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request, 'basic_app/registration.html',
                  {'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})


def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('account'))
    else:
        if request.method == 'POST':
            # First get the username and password supplied
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Django's built-in authentication function:
            user = authenticate(username=username, password=password)

            # If we have a user
            if user:
                # Check it the account is active
                if user.is_active:
                    # Log the user in.
                    login(request, user)
                    # Send the user back to some page.
                    # In this case their homepage.
                    return HttpResponseRedirect(reverse('account'))
                else:
                    # If account is not active:
                    return HttpResponse("Your account is not active.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(
                    username, password))
                msg = '帳號或密碼錯誤'
                return render(request, 'basic_app/login.html', {'msg': msg})

        else:
            # Nothing has been provided for username or password.
            return render(request, 'basic_app/login.html', {})


def owner_detail(request, pk):
    lis = UserProfileInfo.objects.get(user_id=pk)
    print(lis.show)
    if lis.show == 1:
        return render(request, 'basic_app/owner.html', {'lis': lis})
    else:
        return HttpResponseRedirect(reverse('index'))


def change_show(request):
    if request.method == 'POST':
        c = request.POST.get("checkBoxValue")
        print(c)
        if request.user.is_authenticated:
            name = request.user.id
            lis = UserProfileInfo.objects.get(user_id=name)
            if lis.show == 1:
                lis.show = 0
            else:
                lis.show = 1
            lis.save()
    return HttpResponseRedirect(reverse('account'))


def account(request):
    if request.user.is_authenticated:
        name = request.user.id
        #lis = UserProfileInfo.objects.get(user_id = name)
        lis = request.user.userprofileinfo
        a = 'http://www.boloncku.tk/owner/' + str(name)
    # if request.method == 'POST':
    #    pass
        return render(request, 'basic_app/account.html', locals())
    else:
        return HttpResponseRedirect(reverse('index'))


def changepassword(request):
    print(request.method)
    if request.method == 'POST':
        if request.user.is_authenticated:
            #newls = request.POST.get("lsname", None)
            #newfr = request.POST.get("frname", None)
            # User.objects.filter(username=request.user).update(last_name=newls)
            # User.objects.filter(username=request.user).update(first_name=newfr)
            item = request.POST.get("comment", None)
            UserProfileInfo.objects.filter(
                user_id=request.user.id).update(item_show=item)
    return HttpResponseRedirect(reverse('account'))


def contact(request):
    return render(request, 'basic_app/contact.html')


def userlist(request):
    if request.user.is_authenticated:
        changed = False
        user = User.objects.get(username=request.user)
        print(user.email)
        userupdataForm = UserupdataForm(data=request.POST)
        profileupdata_form = UserupdataProfileInfoForm(data=request.POST)
        print(userupdataForm)

        if request.method == 'POST':
            # Get info from "both" forms
            # It appears as one form to the user on the .html page

            # Check to see both forms are valid
            if userupdataForm.is_valid() and profileupdata_form.is_valid():
                # Save User Form to Database
                # Hash the password
                if request.POST['password'] != '':
                    u = User.objects.get(username=request.user)
                    u.set_password(request.POST['password'])
                    u.save()
                if request.POST['email'] != '':
                    User.objects.filter(username=request.user).update(
                        email=request.POST['email'])
                if request.POST['first_name'] != '':
                    User.objects.filter(username=request.user).update(
                        first_name=request.POST['first_name'])
                if request.POST['last_name'] != '':
                    User.objects.filter(username=request.user).update(
                        last_name=request.POST['last_name'])
                # Now we deal with the extra info!

                # Can't commit yet because we still need to manipulate

                # Set One to One relationship between
                # UserForm and UserProfileInfoForm

                if request.POST['gender'] != '':
                    UserProfileInfo.objects.filter(user_id=request.user.id).update(
                        gender=request.POST['gender'])
                if request.POST['FB_site'] != '':
                    UserProfileInfo.objects.filter(user_id=request.user.id).update(
                        FB_site="https://m.me/" + request.POST['FB_site'])
                if request.POST['portfolio_site'] != '':
                    UserProfileInfo.objects.filter(user_id=request.user.id).update(
                        portfolio_site=request.POST['portfolio_site'])
                if request.POST['show_out'] != '':
                    UserProfileInfo.objects.filter(user_id=request.user.id).update(
                        show_out=request.POST['show_out'])
                # Check if they provided a profile picture
                if request.FILES != '':
                    if 'profile_pic' in request.FILES:
                        print('found it')
                        # If yes, then grab it from the POST form reply
                        u_p = UserProfileInfo.objects.get(
                            user_id=request.user.id)
                        u_p.profile_pic = request.FILES['profile_pic']
                        u_p.save()
                    # Now save model
                changed = True

            else:
                # One of the forms was invalid if this else gets called.
                print(userupdataForm.errors, profileupdata_form.errors)

        else:
            # Was not an HTTP post so we just render the forms as blank.
            userupdataForm = UserupdataForm(initial={
                                            'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name})
            profileupdata_form = UserupdataProfileInfoForm(
                initial={'gender': user.userprofileinfo.gender, 'portfolio_site': user.userprofileinfo.portfolio_site, 'FB_site': user.userprofileinfo.FB_site, 'show_out': user.userprofileinfo.show_out})

        return render(request, 'basic_app/userlist.html', locals())
    else:
        return HttpResponseRedirect(reverse('index'))
