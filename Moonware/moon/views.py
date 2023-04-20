# from crypt import methods
import email
from genericpath import exists
from multiprocessing import context
import random
from turtle import pos
from urllib.request import Request
from xmlrpc.client import DateTime
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
import calendar
from dateutil.relativedelta import relativedelta
from django.core.mail import EmailMessage
from django.conf import settings
from django.middleware import csrf
from django.contrib.auth import get_user_model
from django_email_verification import  send_email
from django.core.mail import EmailMultiAlternatives
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from .models import gif, season, view, like, comment, report, pdf, firstImg, secondImg, notification
from .models import avatar, tag, tagLink, feild
from .models import userInfo
from .models import post
from datetime import datetime, timedelta
import os
from io import BytesIO
from openpyxl import Workbook
import csv
import zipfile
import re











# Create your views here.
# common action
# sort post by day
def index(request):
    if request.user.is_authenticated:
        user = request.user
        gifs = gif.objects.all()
        posts = post.objects.all().order_by('-id')
        tags = tag.objects.all().order_by('-id')
        popularPosts = post.objects.order_by('views').reverse()
        mostLikePosts = post.objects.order_by('likes').reverse()
        avatars = avatar.objects.all()
        userInfos = userInfo.objects.filter(user=user).first()
        accessOn = datetime.now().date()
        numberOfNotification = notification.objects.filter(user=user).count()

        topThree = userInfo.objects.order_by('PostAmount').reverse()
        topThreeLength = len(topThree)

        if topThreeLength == 0:
            firstOne = None
            secondOne = None
            thirdOne = None
        elif topThreeLength == 1:
            firstOne = topThree[0]
            secondOne = None
            thirdOne = None
        elif topThreeLength == 2:
            firstOne = topThree[0]
            secondOne = topThree[1]
            thirdOne = None
        elif topThreeLength >= 3:
            firstOne = topThree[0]
            secondOne = topThree[1]
            thirdOne = topThree[2]
        
        postAmmounts = {}
        today = datetime.now().date()

        # 7 days
        valueYDay = []
        for i in range(7):
            date = today - timedelta(days=i)
            postAmmount = post.objects.filter(date=date).count()
            postAmmounts[date] = postAmmount
            valueYDay.append(postAmmount)
        valueYDay.reverse()

        # 4 weeks
        valueYWeek = []
        for i in range(4):
            startDay = today - timedelta(days=i*7+6)
            endDay = today - timedelta(days=i*7)
            postAmmount = post.objects.filter(date__range=[startDay, endDay]).count()
            valueYWeek.append(postAmmount)
        valueYWeek.reverse()

        # 12 months
        valueYMonth = []
        for i in range(12):
            month_start = today.replace(day=1) - relativedelta(months=i)
            month_end = month_start.replace(day=calendar.monthrange(month_start.year, month_start.month)[1])
            postAmmount = post.objects.filter(date__range=[month_start, month_end]).count()
            valueYMonth.append(postAmmount)
        valueYMonth.reverse()        

        context = {'gifs': gifs, 'avatars': avatars, 'userInfos': userInfos, 'posts': posts, "postAmmounts": postAmmounts, "valueYDay": valueYDay, "valueYWeek": valueYWeek, "valueYMonth": valueYMonth, "firstOne": firstOne, "secondOne": secondOne, "thirdOne": thirdOne, "popularPosts": popularPosts, "mostLikePosts": mostLikePosts, "accessOn": accessOn, "numberOfNotification": numberOfNotification, "tags": tags}
        return render(request, 'home.html', context)

    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']                        
            user = User.objects.get(username=username)
            userInfos = userInfo.objects.get(user=user)
            email = user.email
            otp = random.randint(100, 999)
            createOn = datetime.now()
            expireTime = createOn + timedelta(minutes=10)
            formattedExpireTime = expireTime.strftime('%Y-%m-%d %H:%M:%S')

            


            if user is not None and password == userInfos.password:
                # generate element for email
                html_template = 'authenLogin.html'
                mydict = {'username': username, 'otp': otp, 'formattedExpireTime': formattedExpireTime,  'csrf_token': csrf.get_token(request)}
                greeting = 'nice to meet you,' + username
                html_message = render_to_string(html_template, context=mydict)

                    # Create an EmailMultiAlternatives object to send both plain text and HTML messages
                email_message = EmailMultiAlternatives(
                    'babe, please authenticate before we talk',
                    greeting,
                    'quangtute2k2@gmail.com', # replace with your own email address
                    [email],
                )
            
                # Add the HTML message to the EmailMultiAlternatives object
                email_message.attach_alternative(html_message, 'text/html')

                # Send the email
                email_message.send(fail_silently=False)


                # render after do all
                inform = "Hello " + username + " beautiful, check your email to login"
                context = {"inform": inform, "user": user, "userInfos": userInfos}
                return render(request, "informForm.html", context)
            else:
                # render after do all
                inform = "Oh no bro, I can't guess out who are you, maybe your username or password was wrong"
                context = {"inform": inform}
                return render(request, "informForm.html", context)
        return render(request, 'landingPage.html')

def aboutUs(request):
    if request.user.is_authenticated:
        user = request.user
        userInfos = userInfo.objects.get(user=user)
        numberOfNotification = notification.objects.filter(user=user).count()
        context = {'userInfos': userInfos, 'user': user, 'numberOfNotification': numberOfNotification}
        return render(request, 'aboutUS.html', context)
    else:
        return render(request, 'aboutUS.html')

def contact(request):
    if request.user.is_authenticated:
        user = request.user
        userInfos = userInfo.objects.get(user=user)
        numberOfNotification = notification.objects.filter(user=user).count()

        context = {"user": user, "userInfos": userInfos, "numberOfNotification": numberOfNotification}
        if request.method == 'POST':
            reportInserted = request.POST.get('report', 'nothing')
            email = request.POST.get('email', userInfos.email)   
            phone = request.POST.get('phone', "no phone")

            if email == "":
                email = userInfos.email        

    
            reports = report.objects.create(report=reportInserted, user=user, email=email, phone=phone)
            reports.save()

            userInfosOnly = userInfo.objects.filter(type="admin")
            for userss in userInfosOnly:                
                 # generate element for email
                html_template = 'reportEmail.html'
                mydict = {'username': userss.user.username, 'csrf_token': csrf.get_token(request)}
                greeting = 'nice to see u again,' + userss.user.username +', lil admin'
                html_message = render_to_string(html_template, context=mydict)
                email = userss.user.email

                # Create an EmailMultiAlternatives object to send both plain text and HTML messages
                email_message = EmailMultiAlternatives(
                    'Someone need your help',
                    greeting,
                    'quangtute2k2@gmail.com', # replace with your own email address
                    [email],
                )
            
                # Add the HTML message to the EmailMultiAlternatives object
                email_message.attach_alternative(html_message, 'text/html')

                # Send the email
                email_message.send(fail_silently=False)

            # render after do all
            inform = "Dear " + user.username + ", Your report have been sent, have a nice day"
            link = "/"
            linkText = "Back to home"
            context = {"inform": inform, "user": user, "userInfos": userInfos, "link": link, "linkText": linkText}
            return render(request, "informForm.html", context)
        return render(request, "contact.html", context)
    else:
        if request.method == 'POST':
            reportInserted = request.POST.get('report', 'nothing')
            email = request.POST.get('email', "no email")   
            phone = request.POST.get('phone', "no phone")      
    
            reports = report.objects.create(report=reportInserted, user=None, email=email, phone=phone)
            reports.save()

            userInfosOnly = userInfo.objects.filter(type="admin")
            for userss in userInfosOnly:                
                 # generate element for email
                html_template = 'reportEmail.html'
                mydict = {'username': userss.user.username, 'csrf_token': csrf.get_token(request)}
                greeting = 'nice to see u again,' + userss.user.username +', lil admin'
                html_message = render_to_string(html_template, context=mydict)
                email = userss.user.email

                # Create an EmailMultiAlternatives object to send both plain text and HTML messages
                email_message = EmailMultiAlternatives(
                    'Someone need your help',
                    greeting,
                    'quangtute2k2@gmail.com', # replace with your own email address
                    [email],
                )
            
                # Add the HTML message to the EmailMultiAlternatives object
                email_message.attach_alternative(html_message, 'text/html')

                # Send the email
                email_message.send(fail_silently=False)

             # render after do all
            inform = "Dear visiter, Your report have been sent, have a nice day"
            link = "/"
            linkText = "Back to landing page"
            context = {"inform": inform, "link": link, "linkText": linkText}
            return render(request, "informForm.html", context)

        return render(request, "contact.html")

def user_register(request):
    if not request.user.is_authenticated:
        firstFeild = feild.objects.first()
        feilds = feild.objects.all()
        firstAvatar = avatar.objects.first()
        allAvatars = avatar.objects.all()
        context = {'allAvatars' : allAvatars, 'firstAvatar' : firstAvatar, 'firstFeild' : firstFeild, 'feilds' : feilds}
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            avatar_id = request.POST['avatar']
            code = request.POST['code']
            feildImport = request.POST['feild']
            feildGet = feild.objects.get(id=feildImport)
            avatars = avatar.objects.get(id=avatar_id) 
            gifs = gif.objects.get(id=1)           

            # Check if passwords match
            if password1 != password2:
                # render after do all
                inform = "huhu password 1 doesn't match with password 2, try again"
                link = "/register"
                linkText = "Try Again?"
                context = {"inform": inform, "link": link, "linkText": linkText}
                return render(request, "reIputOTP.html", context)

            # Check if username is already taken
            elif User.objects.filter(username=username).exists():
                # render after do all
                inform = "huhu the username has been taken by the faster rabit"
                link = "/register"
                linkText = "Try Again?"
                context = {"inform": inform, "link": link, "linkText": linkText}
                return render(request, "reIputOTP.html", context)

            # Check if email is already taken
            elif User.objects.filter(email=email).exists():
                # render after do all
                inform = "huhu the email has been taken by the faster rabit"
                link = "/register"
                linkText = "Try Again?"
                context = {"inform": inform, "link": link, "linkText": linkText}
                return render(request, "reIputOTP.html", context)

            # Create new user
            else:
                # coordinator
                if code == "anhQuangDepTraiPhongDo":
                    # generate user
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    user.is_active = False
                    user.save()

                    # generate user info
                    userInfos = userInfo.objects.create(email=email, password=password1, avatar=avatars, PostAmount=0, user=user, gif=gifs, type="coordinator", feild=feildGet)
                    userInfos.save()

                    # generate element for email
                    html_template = 'register_email.html'
                    mydict = {'username': username, 'csrf_token': csrf.get_token(request)}
                    greeting = 'nice to meet you,' + username +', lil admin'
                    html_message = render_to_string(html_template, context=mydict)

                    # Create an EmailMultiAlternatives object to send both plain text and HTML messages
                    email_message = EmailMultiAlternatives(
                        'Welcome to moonware, clown',
                        greeting,
                        'quangtute2k2@gmail.com', # replace with your own email address
                        [email],
                    )
                
                    # Add the HTML message to the EmailMultiAlternatives object
                    email_message.attach_alternative(html_message, 'text/html')

                    # Send the email
                    email_message.send(fail_silently=False)

                    # return information for user to activate their account
                    # render after do all
                    inform = "Hey " + username + "! Your account is almost done, let's get back to your gmail to activate it"
                    context = {"inform": inform, "user": user, "userInfos": userInfos}
                    return render(request, "informForm.html", context)


                # admin
                elif code == "anhQuangDepTraiso1":
                    # generate user
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    user.is_staff = True
                    user.is_superuser = True
                    user.is_active = False
                    user.save()

                    # generate user info
                    userInfos = userInfo.objects.create(email=email, password=password1, avatar=avatars, PostAmount=0, user=user, gif=gifs, type="admin")
                    userInfos.save()

                    # generate element for email
                    html_template = 'register_email.html'
                    mydict = {'username': username, 'csrf_token': csrf.get_token(request)}
                    greeting = 'nice to meet you,' + username +', lil admin'
                    html_message = render_to_string(html_template, context=mydict)

                    # Create an EmailMultiAlternatives object to send both plain text and HTML messages
                    email_message = EmailMultiAlternatives(
                        'Welcome to moonware, king',
                        greeting,
                        'quangtute2k2@gmail.com', # replace with your own email address
                        [email],
                    )
                
                    # Add the HTML message to the EmailMultiAlternatives object
                    email_message.attach_alternative(html_message, 'text/html')

                    # Send the email
                    email_message.send(fail_silently=False)

                    # return information for user to activate their account
                    # render after do all
                    inform = "Hey " + username + "! Your account is almost done, let's get back to your gmail to activate it"
                    context = {"inform": inform, "user": user, "userInfos": userInfos}
                    return render(request, "informForm.html", context)

                # staff
                elif code == "anhQuangDepTraiBoDoiThe":
                    # generate user
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    user.is_staff = True
                    user.is_superuser = True
                    user.is_active = False
                    user.save()

                    # generate user info
                    userInfos = userInfo.objects.create(email=email, password=password1, avatar=avatars, PostAmount=0, user=user, gif=gifs, type="manager")
                    userInfos.save()

                    # generate element for email
                    html_template = 'register_email.html'
                    mydict = {'username': username, 'csrf_token': csrf.get_token(request)}
                    greeting = 'nice to meet you,' + username + "lil staff"
                    html_message = render_to_string(html_template, context=mydict)

                    # Create an EmailMultiAlternatives object to send both plain text and HTML messages
                    email_message = EmailMultiAlternatives(
                        'Welcome to moonware, lord',
                        greeting,
                        'quangtute2k2@gmail.com', # replace with your own email address
                        [email],
                    )
                
                    # Add the HTML message to the EmailMultiAlternatives object
                    email_message.attach_alternative(html_message, 'text/html')

                    # Send the email
                    email_message.send(fail_silently=False)

                    # return information for user to activate their account
                    # render after do all
                    inform = "Hey " + username + "! Your account is almost done, let's get back to your gmail to activate it"
                    context = {"inform": inform, "user": user, "userInfos": userInfos}
                    return render(request, "informForm.html", context)

                # normal user
                else:
                    # generate user
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    user.is_active = False
                    user.save()

                    # generate user info
                    userInfos = userInfo.objects.create(email=email, password=password1, avatar=avatars, PostAmount=0, user=user, gif=gifs, feild=feildGet)
                    userInfos.save()

                    # generate element for email
                    html_template = 'register_email.html'
                    mydict = {'username': username, 'csrf_token': csrf.get_token(request)}
                    greeting = 'nice to meet you,' + username
                    html_message = render_to_string(html_template, context=mydict)

                    # Create an EmailMultiAlternatives object to send both plain text and HTML messages
                    email_message = EmailMultiAlternatives(
                        'Welcome to moonware, homie',
                        greeting,
                        'quangtute2k2@gmail.com', # replace with your own email address
                        [email],
                    )
                
                    # Add the HTML message to the EmailMultiAlternatives object
                    email_message.attach_alternative(html_message, 'text/html')

                    # Send the email
                    email_message.send(fail_silently=False)

                    # return information for user to activate their account
                    # render after do all
                    inform = "Hey " + username + "! Your account is almost done, let's get back to your gmail to activate it"
                    context = {"inform": inform, "user": user, "userInfos": userInfos}
                    return render(request, "informForm.html", context)

        return render(request, 'register.html', context)

    else:
        redirect(index)

@csrf_exempt
def activate(request):
    username = request.POST.get('username')
    if username:
        user = User.objects.get(username=username)
        userInfos = userInfo.objects.get(user=user)
        user.is_active = True
        user.save()
        login(request, user) 
        
        # render after do all
        inform = "Hurray " + username + ", your account is activated now, well come to moonware"
        link = "/"
        linkText = "Back to home"
        context = {"inform": inform, "user": user, "userInfos": userInfos, "link": link, "linkText": linkText}
        return render(request, "informForm.html", context)

    return redirect(index)

def checkOtpToLogin(request):
    # username
    if request.GET.get('username') is not None:
        username = request.GET.get('username')
    else:
        username = request.POST.get('username')

    # otp
    if request.GET.get('otp') is not None:
        otp = request.GET.get('otp')
    else:
        otp = request.POST.get('otp')

    # expired time
    if request.GET.get('formattedExpireTime') is not None:
        formattedExpireTime = request.GET.get('formattedExpireTime')
    else:
        formattedExpireTime = request.POST.get('formattedExpireTime')

    # get all thing from post  
    user = User.objects.get(username=username)
    userInfos = userInfo.objects.get(user=user)   
    password = userInfos.password   

    # create elements for comparing timeline for OTP
    expireTime = datetime.strptime(formattedExpireTime, '%Y-%m-%d %H:%M:%S')
    clickedTime = datetime.now()
    formattedclickedTime = clickedTime.strftime('%Y-%m-%d %H:%M:%S')
    formatclickedTime = datetime.strptime(formattedclickedTime, '%Y-%m-%d %H:%M:%S')
    context = {"user": user, "userInfos": userInfos}

    if formatclickedTime <= expireTime:
        if request.method == 'POST':
            otp1 = request.POST['otp1']
            if(otp1 == otp):
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)                
                    return redirect(index)                
            else:
                # render after do all
                inform = "Oyyy " + username + "! I hate you because your OTP was wrong"
                link = "/checkOtpToLogin"
                linkText = "Try Again?"
                context = {"inform": inform, "user": user, "username": username, "userInfos": userInfos, "link": link, "linkText": linkText, "formattedExpireTime": formattedExpireTime, "otp": otp}
                return render(request, "reIputOTP.html", context)
        return render(request, "otpToLogin.html", context)
    else:
        # render after do all
        inform = "Oyyy " + username + "! Your OTP is invalid now because you are late as turtle"
        context = {"inform": inform}
        return render(request, "informForm.html", context)



















# forgot password, send otp to re-new password
def forgotPassword(request):
    if request.method == 'POST':
        otp = random.randint(100, 999)
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:         
            # render after do all
            inform = "Well, actually I don't know who actually u are, check if registered email is right"
            link = "/forgotPassword"
            linkText = "Try Again?"
            context = {"inform": inform, "link": link, "linkText": linkText,}
            return render(request, "reIputOTP.html", context)

        username = user.username
        createOn = datetime.now()
        expireTime = createOn + timedelta(minutes=10)
        formattedExpireTime = expireTime.strftime('%Y-%m-%d %H:%M:%S')

        # generate element for email
        html_template = 'forgotPassword.html'
        mydict = {'username': username, 'otp': otp, 'formattedExpireTime': formattedExpireTime, 'csrf_token': csrf.get_token(request)}
        greeting = 'Hallo ' + username
        html_message = render_to_string(html_template, context=mydict)

         # Create an EmailMultiAlternatives object to send both plain text and HTML messages
        email_message = EmailMultiAlternatives(
            'Come on, it just username and password, just 2 lines',
            greeting,
            'quangtute2k2@gmail.com', # replace with your own email address
            [email],
        )
    
        # Add the HTML message to the EmailMultiAlternatives object (HTML Email)
        email_message.attach_alternative(html_message, 'text/html')

        # Send the email
        email_message.send(fail_silently=False)

        # return information for user to activate their account (ask user to check their mail)
        return render(request, "checkForPass.html", {'user': user})

    # (add email html)
    return render(request, 'password.html')

@csrf_exempt
def checkOtp(request):
    # username
    if request.GET.get('username') is not None:
        username = request.GET.get('username')
    else:
        username = request.POST.get('username')

    # otp
    if request.GET.get('otp') is not None:
        otp = request.GET.get('otp')
    else:
        otp = request.POST.get('otp')

    # expired time
    if request.GET.get('formattedExpireTime') is not None:
        formattedExpireTime = request.GET.get('formattedExpireTime')
    else:
        formattedExpireTime = request.POST.get('formattedExpireTime')


    expireTime = datetime.strptime(formattedExpireTime, '%Y-%m-%d %H:%M:%S')
    clickedTime = datetime.now()
    formattedclickedTime = clickedTime.strftime('%Y-%m-%d %H:%M:%S')
    formatclickedTime = datetime.strptime(formattedclickedTime, '%Y-%m-%d %H:%M:%S')

    context = {"username": username, "otp": otp, "formattedExpireTime": formattedExpireTime}

    if formatclickedTime <= expireTime:
        if request.method == 'POST':
            otp1 = request.POST['otp1']
            if(otp1 == otp):
                user = User.objects.get(username=username)
                userInfos = userInfo.objects.get(user=user)
                password = userInfos.password
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect(newPass)
                else:
                    # render after do all
                    inform = "Oyyy " + username + "! Who actually the fuck are u?"                    
                    context = {"inform": inform, "formattedExpireTime": formattedExpireTime, "otp": otp, }
                    return render(request, "reIputOTP.html", context)
            else:
                # render after do all
                inform = "Oyyy " + username + "! I hate you because your OTP was wrong"
                link = "/checkOtp"
                linkText = "Try Again?"
                context = {"inform": inform, "link": link, "linkText": linkText, "username": username, "formattedExpireTime": formattedExpireTime, "otp": otp}
                return render(request, "reIputOTP.html", context)
                
        return render(request, "checkOtp.html", context)
    else:
        # render after do all
        inform = "Oyyy " + username + "! Your OTP is invalid now because you are late as turtle"
        context = {"inform": inform}
        return render(request, "informForm.html", context)

def newPass(request):
    user = request.user
    userInfos = userInfo.objects.get(user=user)
    context = {'user': user, 'userInfos': userInfos}
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if(password1==password2):
            user.set_password(password1)
            user.save()
            userInfos.password = password1
            userInfos.save()
            return redirect(passChanged)
        else:
            return redirect(newPass)

    return render(request, "newPass.html", context)

def passChanged(request):
    user = request.user
    username = user.username
    context = {'username': username}
    logout(request)
    return render(request, "passwordChanged.html", context)












# coordinator
def coordinator(request):
    if request.user.is_authenticated:
        user = request.user
        userInfos = userInfo.objects.get(user=user)
        userFeild = userInfos.feild
        numberOfNotification = notification.objects.filter(user=user).count()
        posts = post.objects.filter(feild=userFeild)
        tags = tag.objects.all().order_by('-id')
        postLikeFeildAmmounts = 0
        postViewFeildAmmounts = 0

        postFeildAmmounts = posts.count()

        for postSingle in posts:
            postLikeFeildAmmounts = postLikeFeildAmmounts + postSingle.likes

        for postSingle in posts:
            postViewFeildAmmounts = postViewFeildAmmounts + postSingle.views

        postAmmounts = {}
        today = datetime.now().date()

        # 7 days
        valueYDay = []
        for i in range(7):
            date = today - timedelta(days=i)
            postAmmount = posts.filter(date=date).count()
            postAmmounts[date] = postAmmount
            valueYDay.append(postAmmount)
        valueYDay.reverse()

        # 4 weeks
        valueYWeek = []
        for i in range(4):
            startDay = today - timedelta(days=i*7+6)
            endDay = today - timedelta(days=i*7)
            postAmmount = posts.filter(date__range=[startDay, endDay]).count()
            valueYWeek.append(postAmmount)
        valueYWeek.reverse()

        # 12 months
        valueYMonth = []
        for i in range(12):
            month_start = today.replace(day=1) - relativedelta(months=i)
            month_end = month_start.replace(day=calendar.monthrange(month_start.year, month_start.month)[1])
            postAmmount = posts.filter(date__range=[month_start, month_end]).count()
            valueYMonth.append(postAmmount)
        valueYMonth.reverse()   

        context = {"user": user, "userInfos": userInfos, "numberOfNotification": numberOfNotification, "posts": posts, "tags": tags, "valueYDay": valueYDay, "valueYWeek": valueYWeek, "valueYMonth": valueYMonth, "postFeildAmmounts": postFeildAmmounts, "postLikeFeildAmmounts": postLikeFeildAmmounts, "postViewFeildAmmounts": postViewFeildAmmounts}
        return render(request, "coordinator.html", context)
    else:
        return redirect(index)

def addNewTags(request):
    if request.method == 'POST':
        tagname = request.POST.get('tag', '')

        if tagname == '':
            # render after do all
            inform = "please add name to tag before u add it"
            link = "/coordinator"
            linkText = "Try Again?"
            context = {"inform": inform, "link": link, "linkText": linkText}
            return render(request, "reIputOTP.html", context)
        else:
            tags = tag.objects.create(name=tagname)
            tags.save()

            return redirect(coordinator)

def deletePostCoo(request):
    if request.method == 'POST':
        user = request.user
        userInfos = userInfo.objects.get(user=user)
        postId = request.POST.get("postId")
        posts = post.objects.get(id=postId)  
        postOwner = posts.user
        postOwnerInfo = userInfo.objects.get(user=postOwner) 

        # first image
        if posts.fistImage is not None:
            img1 = firstImg.objects.get(id=posts.fistImage.id)
            img1Url = img1.img.name
            img1.delete()
            os.remove(img1Url)
        

        # second one
        if posts.secondImage is not None:
            img2 = secondImg.objects.get(id=posts.secondImage.id)
            img2Url = img2.img.name
            img2.delete()
            os.remove(img2Url)
        

        # and pdf
        if posts.pdf is not None:
            pdfFile = pdf.objects.get(id=posts.pdf.id)
            pdfFileUrl = pdfFile.pdf.name
            pdfFile.delete()
            os.remove(pdfFileUrl)

        

        posts.delete()

        postOwnerInfo.PostAmount = postOwnerInfo.PostAmount - 1
        postOwnerInfo.save()

        # render after do all
        inform = "Hey " + user.username + " darling, the post that you deleted should be really sad in it's graves"
        link = "/"
        linkText = "Back to Home?"
        context = {"inform": inform, "user": user, "userInfos": userInfos, "link": link, "linkText": linkText}
        return render(request, "informForm.html", context)


























# change password regular
def otpToChangePass(request):
    # user info
    user = request.user
    username = user.username
    email = user.email
    userInfos = userInfo.objects.get(user=user)

    # pass for changing process
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    password3 = request.POST.get('password3')

    # compare current password
    if password1 == userInfos.password:
        # compare new and retyped new password
        if password2 == password3:
            # otp
            otp = random.randint(100, 999)

            # create expired time
            createOn = datetime.now()
            expireTime = createOn + timedelta(minutes=2)
            formattedExpireTime = expireTime.strftime('%Y-%m-%d %H:%M:%S')

            # generate element for email
            html_template = 'otpToChangePass.html'
            mydict = {'username': username, 'otp': otp, 'password1': password1, 'password2': password2, 'password3': password3, 'formattedExpireTime': formattedExpireTime, 'csrf_token': csrf.get_token(request)}
            greeting = 'Hallo ' + username
            html_message = render_to_string(html_template, context=mydict)

            # Create an EmailMultiAlternatives object to send both plain text and HTML messages
            email_message = EmailMultiAlternatives(
                'OTP for new password',
                greeting,
                'quangtute2k2@gmail.com', # replace with your own email address
                [email],
            )

            # Add the HTML message to the EmailMultiAlternatives object (HTML Email)
            email_message.attach_alternative(html_message, 'text/html')

            # Send the email
            email_message.send(fail_silently=False)

            # render after do all
            inform = "check out your email to get OTP code"
            context = {"inform": inform, "user": user, "userInfos": userInfos}
            return render(request, "informForm.html", context)
        else:
            # render after do all
            inform = "Oh no " + username + " darling, seem like your new password dont match your 2nd typed password"
            link = "/account"
            linkText = "Try Again?"
            context = {"inform": inform, "user": user, "userInfos": userInfos, "link": link, "linkText": linkText}
            return render(request, "informForm.html", context)
    else:
        # render after do all
        inform = "Oh no " + password1 +","+userInfos.password+ " darling, do you got any problem with your alzheimer on remembering your password"
        link = "/account"
        linkText = "Try Again?"
        context = {"inform": inform, "user": user, "userInfos": userInfos, "link": link, "linkText": linkText}
        return render(request, "informForm.html", context)

@csrf_exempt
def checkOtpToPassword(request):
    # get all thing from post
    username = request.GET.get('username')
    otp = request.GET.get('otp')
    password2 = request.GET.get('password2')
    formattedExpireTime = request.GET.get('formattedExpireTime')

    user = User.objects.get(username=username)
    userInfos = userInfo.objects.get(user=user)

    # create elements for comparing timeline for OTP
    expireTime = datetime.strptime(formattedExpireTime, '%Y-%m-%d %H:%M:%S')
    clickedTime = datetime.now()
    formattedclickedTime = clickedTime.strftime('%Y-%m-%d %H:%M:%S')
    formatclickedTime = datetime.strptime(formattedclickedTime, '%Y-%m-%d %H:%M:%S')
    context = {"user": user, "userInfos": userInfos}

    if expireTime >= formatclickedTime:
        if request.method == 'POST':
            otp1 = request.POST['otp1']
            if otp == otp1:
                user = User.objects.get(username=username)
                user.set_password(password2)
                user.save()
                userInfos = userInfo.objects.get(user=user)
                userInfos.password = password2
                userInfos.save()
                logout(request)

                # render after do all
                inform = "Yo " + username + ", it's finished, you can back to homepage and login to continues"
                link = "/"
                linkText = "Back to home"
                context = {"inform": inform, "user": user, "userInfos": userInfos, "link": link, "linkText": linkText}
                return render(request, "informForm.html", context)
            else:
                # render after do all
                inform = "Oh no " + username + " darling, your OTP was wrong, are you hacker? or you got some alzheimer?"
                link = "/account"
                linkText = "Try Again?"
                context = {"inform": inform, "link": link, "linkText": linkText, "username": username, "formattedExpireTime": formattedExpireTime, "otp": otp}
                return render(request, "reIputOTP.html", context)
        return render (request, "checkOtp.html", context)

    else:
        # render after do all
        inform = "Oh no " + username + " darling, your OTP is invalid now, you should do it faster"
        link = "/account"
        linkText = "Try Again?"
        context = {"inform": inform, "user": user, "userInfos": userInfos, "link": link, "linkText": linkText}
        return render(request, "informForm.html", context)

def finallyChangePass(request):
    # get user and user info
    user = request.user
    userInfos = userInfo.objects.get(user=user)

    # get new and old password
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    password3 = request.POST.get('password3')

    if (password1 == userInfos.password):
        if(password2 == password3):
            user.set_password(password2)
            user.save()
            userInfos.password = password2
            userInfos.save()
            return redirect(passChanged)
        return redirect(account)
    return redirect(account)





















# some bullshit functions
def updateGif (request, pk):
    user = request.user.pk
    gifs = get_object_or_404(gif, pk=pk)
    userInfos = userInfo.objects.filter(user=user).first()
    userInfos.gif = gifs
    userInfos.save()
    return redirect(index)

def updateAvatar(request, pk):
    avatars = get_object_or_404(avatar, pk=pk)
    user = request.user
    userInfos = userInfo.objects.get(user=user)
    userInfos.avatar = avatars
    userInfos.save()
    return redirect(account)


def notificate(request):
    if request.user.is_authenticated:
        user = request.user
        userInfos = userInfo.objects.get(user=user)
        notifications = notification.objects.filter(user=user)
        numberOfNotification = notification.objects.filter(user=user).count()
        
        context = {"user": user, "userInfos": userInfos, "notifications": notifications, "numberOfNotification": numberOfNotification,}

        return render(request, "notification.html", context)
    else:
        return redirect(index)

def pinNotificate(request, pk):
    notifications = get_object_or_404(notification, pk=pk)
    notifications.pinned = True
    notifications.save()
    return redirect(notificate)

def unPinNotificate(request, pk):
    notifications = get_object_or_404(notification, pk=pk)
    notifications.pinned = False
    notifications.save()
    return redirect(notificate)

def deleteNotification(request, pk):
    notifications = get_object_or_404(notification, pk=pk)
    notifications.delete()
    return redirect(notificate)

def showByTag(request,pk):
    user = request.user
    userInfos = userInfo.objects.get(user=user)
    numberOfNotification = notification.objects.filter(user=user).count()
    tags = get_object_or_404(tag, pk=pk)
    tagLinks = tagLink.objects.filter(tag=tags)
    user = request.user
    context={"tagLinks": tagLinks, "user": user, "tags": tags, "user": user, "userInfos": userInfos, "numberOfNotification": numberOfNotification}

    return render(request, "showByTag.html", context)























# user managements & actions
def account(request):
    user = request.user
    avatars = avatar.objects.all() 
    userInfos = userInfo.objects.get(user=user)
    numberOfNotification = notification.objects.filter(user=user).count()
    context = {'user': user, 'userInfos': userInfos, 'avatars': avatars, 'numberOfNotification': numberOfNotification}
    return render(request, "account.html", context)



def storage(request):
    if request.user.is_authenticated:
        user = request.user
        userInfos = userInfo.objects.get(user=user)
        posts = post.objects.all()
        accessOn = datetime.now().date()
        tags = tag.objects.all()
        tagLinks = tagLink.objects.all()
        formataccessOn = accessOn.strftime('%Y-%m-%d')
        seasons = season.objects.filter(firstDeadline__gte=formataccessOn)
        numberOfNotification = notification.objects.filter(user=user).count()

        context = {'userInfos': userInfos, 'posts': posts, 'user': user, 'seasons': seasons, 'formataccessOn': formataccessOn, 'accessOn': accessOn, 'numberOfNotification': numberOfNotification, 'tags': tags, 'tagLinks': tagLinks}

        return render(request, 'storage.html', context)
    else:
        return redirect(index)

def createPost(request):
    if request.method == 'POST':
            user = request.user
            userInfos = userInfo.objects.get(user=user)
            seasonTitle = request.POST["seasonTitle"]
            feilds = userInfos.feild

            if seasonTitle != "none":            
                seasons = season.objects.get(title=seasonTitle)
                title = request.POST["title"]
                content = request.POST["content"]
                youTube = request.POST["youTube"]

                fistImage = request.FILES.get("fistImage", "")
                if fistImage == "":
                    fistImage2 = None 
                else:            
                    fistImage2 = firstImg.objects.create(img=fistImage)
                    fistImage2.save()

                secondImage = request.FILES.get("secondImage", "")
                if secondImage == "":
                    secondImage2 = None 
                else:
                    secondImage2 = secondImg.objects.create(img=secondImage)
                    secondImage2.save()

                pdfUpload = request.FILES.get("pdf", "")
                if pdfUpload == "":
                    pdf2 = None 
                else:
                    pdf2 = pdf.objects.create(pdf=pdfUpload)
                    pdf2.save()

                createOn = datetime.now()

                posts = post.objects.create(title=title, content=content, youTube=youTube, pdf=pdf2, fistImage=fistImage2, secondImage=secondImage2, date=createOn, user=user, season=seasons, feild=feilds)
                posts.save()

                userInfos.PostAmount = userInfos.PostAmount + 1
                userInfos.save()

                coordinators = userInfo.objects.filter(type="coordinator")
                userInfosOnly = coordinators.filter(feild=feilds)
                for userss in userInfosOnly:                
                    # generate element for email
                    html_template = 'coordinatorEmail.html'
                    mydict = {'username': userss.user.username, 'csrf_token': csrf.get_token(request)}
                    greeting = 'someone posted new post,' + userss.user.username +', lil coordinator'
                    html_message = render_to_string(html_template, context=mydict)
                    email = userss.user.email

                    # Create an EmailMultiAlternatives object to send both plain text and HTML messages
                    email_message = EmailMultiAlternatives(
                        'Someone add new post',
                        greeting,
                        'quangtute2k2@gmail.com', # replace with your own email address
                        [email],
                    )
                
                    # Add the HTML message to the EmailMultiAlternatives object
                    email_message.attach_alternative(html_message, 'text/html')

                    # Send the email
                    email_message.send(fail_silently=False)

                    # render after do all
                    inform = "Hehe " + user.username + " handsome, you have just create new post? nice nice hehe"
                    link = "/"
                    linkText = "Home"
                    context = {"inform": inform, "user": user, "userInfos": userInfos, "link": link, "linkText": linkText}
                    return render(request, "informForm.html", context)
            else:
                # render after do all
                inform = "You know what? " + user.username + " stupid, when it said no season available, there actually no season available"
                link = "/"
                linkText = "Home"
                context = {"inform": inform, "user": user, "userInfos": userInfos, "link": link, "linkText": linkText}
                return render(request, "informForm.html", context)

def updatePost(request):
    if request.method == 'POST':
            user = request.user
            userInfos = userInfo.objects.get(user=user)
            postId = request.POST["postId"]
            postObject = post.objects.get(id=postId)
            postFilter = post.objects.filter(id=postId)

            title = request.POST["title"]
            content = request.POST["content"]
            youTube = request.POST["youTube"]

            fistImage = request.FILES.get("fistImage", "")
            secondImage = request.FILES.get("secondImage", "")
            newPdf = request.FILES.get("pdf", "")
            print(request.FILES)

            # first img update
            if fistImage != "":
                if postObject.fistImage is not None:
                    img = firstImg.objects.get(id=postObject.fistImage.id)
                    imgUrl = img.img.name
                    img.delete()
                    os.remove(imgUrl)
                fistImage2 = firstImg.objects.create(img=fistImage)
                fistImage2.save()
                postObject.fistImage = fistImage2
                postObject.save()
                

            # second img update
            if secondImage != "":
                if postObject.secondImage is not None:
                    img = secondImg.objects.get(id=postObject.secondImage.id)
                    imgUrl = img.img.name
                    img.delete()
                    os.remove(imgUrl)
                secondImage2 = secondImg.objects.create(img=secondImage)
                secondImage2.save()
                postObject.secondImage = secondImage2
                postObject.save()
                

            # pdf update
            if newPdf != "":
                if postObject.pdf is not None:
                    oldPdf = pdf.objects.get(id=postObject.pdf.id)
                    pdfUrl = oldPdf.pdf.name
                    oldPdf.delete()
                    os.remove(pdfUrl)
                pdf2 = pdf.objects.create(pdf=newPdf)
                pdf2.save()
                postObject.pdf = pdf2
                postObject.save()
                
                
            
            postFilter.update(title=title, content=content, youTube=youTube)

            # render after do all
            inform = "Boom boom " + user.username + " otimus prime! new update? ready to dominate human with that?"
            link = "/"
            linkText = "Back to home"
            context = {"inform": inform, "user": user, "userInfos": userInfos, "link": link, "linkText": linkText}
            return render(request, "informForm.html", context)

def deletePost(request):
    user = request.user
    userInfos = userInfo.objects.get(user=user)
    postId = request.POST.get("postId")
    posts = post.objects.get(id=postId)    

    # first image
    if posts.fistImage is not None:
        img1 = firstImg.objects.get(id=posts.fistImage.id)
        img1Url = img1.img.name
    

    # second one
    if posts.secondImage is not None:
        img2 = secondImg.objects.get(id=posts.secondImage.id)
        img2Url = img2.img.name
    

    # and pdf
    if posts.pdf is not None:
        pdfFile = pdf.objects.get(id=posts.pdf.id)
        pdfFileUrl = pdfFile.pdf.name
    

    # removing and deleting
    img1.delete()
    os.remove(img1Url)

    img2.delete()
    os.remove(img2Url)

    pdfFile.delete()
    os.remove(pdfFileUrl)

    posts.delete()

    userInfos.PostAmount = userInfos.PostAmount - 1
    userInfos.save()

     # render after do all
    inform = "Hey " + user.username + " darling, the post that you deleted should be really sad in it's graves"
    link = "/"
    linkText = "Back to Home?"
    context = {"inform": inform, "user": user, "userInfos": userInfos, "link": link, "linkText": linkText}
    return render(request, "informForm.html", context)

def postDetail(request, pk):
    user = request.user
    userInfos = userInfo.objects.get(user=user)
    posts = get_object_or_404(post, pk=pk)
    # views = view.objects.filter(user=user, post=posts)

    # for other comments
    allUser = User.objects.all()
    allUserInfo = userInfo.objects.all()
    comments = comment.objects.filter(post=posts)
    commentNumb = comment.objects.filter(post=posts).count()
    accessOn = datetime.now().date()
    tagLinks = tagLink.objects.filter(post=posts)

    views = view.objects.filter(user=user, post=posts)
    likes = like.objects.filter(user=user, post=posts)

    numberOfNotification = notification.objects.filter(user=user).count()

    if not views.exists():
        views = view.objects.create(user=user, post=posts)
        views.save()
        posts.views = posts.views + 1
        posts.save()

    if not likes.exists():
        likes = like.objects.create(user=user, post=posts)
        likes.save()

    video_id = posts.youTube.split("v=")[-1].split("&")[0]
    embed_link = f"https://www.youtube.com/embed/{video_id}?autoplay=1"
    likes = like.objects.get(user=user, post=posts)
    context = {"posts": posts, "embed_link": embed_link, "likes": likes, "userInfos": userInfos, "allUser": allUser, "allUserInfo": allUserInfo, "comments": comments, "commentNumb": commentNumb, "accessOn": accessOn, "numberOfNotification": numberOfNotification, "tagLinks": tagLinks}
    return render(request, "postDetail.html", context)

def addTags(request, pk):
    user = request.user
    userInfos = userInfo.objects.get(user=user)
    numberOfNotification = notification.objects.filter(user=user).count()
    posts = get_object_or_404(post, pk=pk)
    tagLinks = tagLink.objects.filter(post=posts)
    tags = tag.objects.all()

    context = {"posts": posts, "tagLinks": tagLinks, "tags": tags, "user": user, "userInfos": userInfos, "numberOfNotification": numberOfNotification,}
    return render(request, "addtag.html", context)

def addTagsFinal(request):
    if request.method == 'POST':
        postId = request.POST.get("postId")
        tagId = request.POST.get("tagId")
        posts = post.objects.get(id=postId)
        tags = tag.objects.get(id=tagId)

        tagLinks = tagLink.objects.create(post=posts, tag=tags)
        tagLinks.save()

        return redirect(addTags, pk=postId)

def deleteTag(request):
    if request.method == 'POST':       
        tagLinkId = request.POST.get("tagLinkId")        
        tagLinks = tagLink.objects.get(id=tagLinkId)
        postId = tagLinks.post.id
        tagLinks.delete()

        return redirect(addTags, pk=postId)

def likeOrDislike(request):
    likee = request.GET.get("like")
    dislike = request.GET.get("dislike")
    postId = request.GET.get("postId")
    posts = post.objects.get(id=postId)
    user = request.user

    username = posts.user.username
    email = posts.user.email  

    likes = like.objects.get(user=user, post=posts)
    if likee == "1" and dislike == "0":
        if likes.like == False and likes.dislike == False:
            # like +
            posts.likes = posts.likes + 1
            likes.like = True
            posts.save()
            likes.save()

            # send notification
            title = user.username + " liked your post"
            postOwner = posts.user
            newNotification = notification.objects.create(title=title, user=postOwner, post=posts)
            newNotification.save()

            # generate element for email
            html_template = 'notificationEmail.html'
            mydict = {'username': username, 'csrf_token': csrf.get_token(request)}
            greeting = 'Hallo' + username +', somethings just happened'
            html_message = render_to_string(html_template, context=mydict)

            # Create an EmailMultiAlternatives object to send both plain text and HTML messages
            email_message = EmailMultiAlternatives(
                'hallo babe, somethings happened on your post',
                greeting,
                'quangtute2k2@gmail.com', # replace with your own email address
                [email],
            )

             # Add the HTML message to the EmailMultiAlternatives object (HTML Email)
            email_message.attach_alternative(html_message, 'text/html')

            # Send the email
            email_message.send(fail_silently=False)


        elif likes.like == False and likes.dislike == True:
            # like + dislike -
            posts.likes = posts.likes + 1
            posts.dislikes = posts.dislikes - 1
            likes.like = True
            likes.dislike = False
            posts.save()
            likes.save()

            # send notification
            title = user.username + " liked your post"
            postOwner = posts.user
            newNotification = notification.objects.create(title=title, user=postOwner, post=posts)
            newNotification.save()

            title = user.username + " disliked your post"
            postOwner = posts.user
            oldNotification = notification.objects.get(title=title, user=postOwner, post=posts)
            oldNotification.delete()

            # generate element for email
            html_template = 'notificationEmail.html'
            mydict = {'username': username, 'csrf_token': csrf.get_token(request)}
            greeting = 'Hallo' + username +', somethings just happened'
            html_message = render_to_string(html_template, context=mydict)

            # Create an EmailMultiAlternatives object to send both plain text and HTML messages
            email_message = EmailMultiAlternatives(
                'hallo babe, somethings happened on your post',
                greeting,
                'quangtute2k2@gmail.com', # replace with your own email address
                [email],
            )

             # Add the HTML message to the EmailMultiAlternatives object (HTML Email)
            email_message.attach_alternative(html_message, 'text/html')

            # Send the email
            email_message.send(fail_silently=False)

        elif  likes.like == True and likes.dislike == False:
            # like - 
            posts.likes = posts.likes - 1
            likes.like = False
            posts.save()
            likes.save()

            # send notification
            title = user.username + " liked your post"
            postOwner = posts.user
            oldNotification = notification.objects.get(title=title, user=postOwner, post=posts)
            oldNotification.delete()

    elif likee == "0" and dislike == "1":
        if likes.like == False and likes.dislike == False:
            # dislike +
            posts.dislikes = posts.dislikes + 1
            likes.dislike = True
            posts.save()
            likes.save()

            # send notification
            title = user.username + " disliked your post"
            postOwner = posts.user
            newNotification = notification.objects.create(title=title, user=postOwner, post=posts)
            newNotification.save()

            # generate element for email
            html_template = 'notificationEmail.html'
            mydict = {'username': username, 'csrf_token': csrf.get_token(request)}
            greeting = 'Hallo' + username +', somethings just happened'
            html_message = render_to_string(html_template, context=mydict)

            # Create an EmailMultiAlternatives object to send both plain text and HTML messages
            email_message = EmailMultiAlternatives(
                'hallo babe, somethings happened on your post',
                greeting,
                'quangtute2k2@gmail.com', # replace with your own email address
                [email],
            )

             # Add the HTML message to the EmailMultiAlternatives object (HTML Email)
            email_message.attach_alternative(html_message, 'text/html')

            # Send the email
            email_message.send(fail_silently=False)

        elif likes.like == True and likes.dislike == False:
            # like - dislike +
            posts.likes = posts.likes - 1
            posts.dislikes = posts.dislikes + 1
            likes.like = False
            likes.dislike = True
            posts.save()
            likes.save()

            # send notification
            title = user.username + " disliked your post"
            postOwner = posts.user
            newNotification = notification.objects.create(title=title, user=postOwner, post=posts)
            newNotification.save()

            title = user.username + " liked your post"
            postOwner = posts.user
            oldNotification = notification.objects.get(title=title, user=postOwner, post=posts)
            oldNotification.delete()

            # generate element for email
            html_template = 'notificationEmail.html'
            mydict = {'username': username, 'csrf_token': csrf.get_token(request)}
            greeting = 'Hallo' + username +', somethings just happened'
            html_message = render_to_string(html_template, context=mydict)

            # Create an EmailMultiAlternatives object to send both plain text and HTML messages
            email_message = EmailMultiAlternatives(
                'hallo babe, somethings happened on your post',
                greeting,
                'quangtute2k2@gmail.com', # replace with your own email address
                [email],
            )

             # Add the HTML message to the EmailMultiAlternatives object (HTML Email)
            email_message.attach_alternative(html_message, 'text/html')

            # Send the email
            email_message.send(fail_silently=False)

        elif  likes.like == False and likes.dislike == True:
            # dislike - 
            posts.dislikes = posts.dislikes - 1
            likes.dislike = False
            posts.save()
            likes.save()

            # send notification
            title = user.username + " disliked your post"
            postOwner = posts.user
            oldNotification = notification.objects.get(title=title, user=postOwner, post=posts)
            oldNotification.delete()

    
    return redirect('postDetail', pk=postId)

def createComment(request):
    commentLine = request.GET.get("comment")
    postId = request.GET.get("postId")
    posts = post.objects.get(id=postId)
    user = request.user
    username = posts.user.username
    email = posts.user.email

    comments = comment.objects.create(user=user, post=posts, comment=commentLine)
    comments.save()

    title = user.username + " commented your post"
    postOwner = posts.user
    commentNotify = notification.objects.create(title=title, user=postOwner, post=posts)
    commentNotify.save()

    # generate element for email
    html_template = 'notificationEmail.html'
    mydict = {'username': username, 'csrf_token': csrf.get_token(request)}
    greeting = 'Hallo' + username +', somethings just happened'
    html_message = render_to_string(html_template, context=mydict)

    # Create an EmailMultiAlternatives object to send both plain text and HTML messages
    email_message = EmailMultiAlternatives(
        'hallo babe, somethings happened on your post',
        greeting,
        'quangtute2k2@gmail.com', # replace with your own email address
        [email],
    )

        # Add the HTML message to the EmailMultiAlternatives object (HTML Email)
    email_message.attach_alternative(html_message, 'text/html')

    # Send the email
    email_message.send(fail_silently=False)

    return redirect('postDetail', pk=postId)

















# login for changing password (this one maybe wont be used on website, but I'm not pretty sure so I leave it there)
def loginToChangePass(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)                                
                avatars = avatar.objects.all()
                userInfos = userInfo.objects.get(user=user)
                context = {'avatars': avatars, 'userInfos': userInfos}
                return render(request, 'changingPass.html', context)
            else:
                messages.error(request, 'Invalid username or password')
        return render(request, 'loginForChangingPass.html')
    else:
        user = request.user
        avatars = avatar.objects.all()
        userInfos = userInfo.objects.get(user=user)
        context = {'avatars': avatars, 'userInfos': userInfos}
        return render(request, 'changingPass.html', context)














# log out
def user_logout(request):
    logout(request)
    return redirect(index)











def exportData(request):
    user = request.user
    userInfos = userInfo.objects.get(user=user)
    numberOfNotification = notification.objects.filter(user=user).count()
    if userInfos.type == "manager":
        seasons = season.objects.all()
        context = {"user": user, "userInfos": userInfos, "numberOfNotification": numberOfNotification, "seasons": seasons}
        return render(request, "exportData.html", context)
    else:
         # render after do all
        inform = "Sorry " + user.username + " , you have to be manager to use this function. Now, get back home"
        link = "../"
        linkText = "back Home"
        context = {"inform": inform, "user": user, "userInfos": userInfos, "link": link, "linkText": linkText}
        return render(request, "informForm.html", context)


# excel file
def exportExcel(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        seasonId = request.POST.get('seasonId')

        if seasonId == 'all':
            myclass_data = post.objects.all()
        else:
            seasons = season.objects.get(id=seasonId)
            myclass_data = post.objects.filter(season=seasons)

        response = HttpResponse(content_type='text/csv')
        if name == '':
            response['Content-Disposition'] = 'attachment; filename="myclass_data.csv"'
        else:
            filename = name+".csv"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        # Create an Excel workbook
        wb = Workbook()
        # Get the default sheet
        sheet = wb.active
        
        # Write data to the sheet
        for row in myclass_data:
            if row.fistImage is not None and row.secondImage is not None and row.pdf is not None:                
                # Append row data to the sheet
                sheet.append([row.title, row.content, row.views, row.likes, row.dislikes, row.youTube, row.pdf.pdf.name, row.fistImage.img.name, row.secondImage.img.name, row.date, row.user.username, row.season.title])  # Replace field1, field2, field3 with the actual field names of MyClass model
            
            elif row.fistImage is None and row.secondImage is not None and row.pdf is not None:                
                # Append row data to the sheet
                sheet.append([row.title, row.content, row.views, row.likes, row.dislikes, row.youTube, row.pdf.pdf.name, "none", row.secondImage.img.name, row.date, row.user.username, row.season.title])  # Replace field1, field2, field3 with the actual field names of MyClass model
            elif row.fistImage is not None and row.secondImage is None and row.pdf is not None:                
                # Append row data to the sheet
                sheet.append([row.title, row.content, row.views, row.likes, row.dislikes, row.youTube, row.pdf.pdf.name, row.fistImage.img.name, "none", row.date, row.user.username, row.season.title])  # Replace field1, field2, field3 with the actual field names of MyClass model
            elif row.fistImage is not None and row.secondImage is not None and row.pdf is None:                
                # Append row data to the sheet
                sheet.append([row.title, row.content, row.views, row.likes, row.dislikes, row.youTube, "none", row.fistImage.img.name, row.secondImage.img.name, row.date, row.user.username, row.season.title])  # Replace field1, field2, field3 with the actual field names of MyClass model
            
            elif row.fistImage is None and row.secondImage is None and row.pdf is not None:                
                # Append row data to the sheet
                sheet.append([row.title, row.content, row.views, row.likes, row.dislikes, row.youTube, row.pdf.pdf.name, "none", "none", row.date, row.user.username, row.season.title])  # Replace field1, field2, field3 with the actual field names of MyClass model
            elif row.fistImage is not None and row.secondImage is None and row.pdf is None:                
                # Append row data to the sheet
                sheet.append([row.title, row.content, row.views, row.likes, row.dislikes, row.youTube, "none", row.fistImage.img.name, "none", row.date, row.user.username, row.season.title])  # Replace field1, field2, field3 with the actual field names of MyClass model
            elif row.fistImage is None and row.secondImage is not None and row.pdf is None:                
                # Append row data to the sheet
                sheet.append([row.title, row.content, row.views, row.likes, row.dislikes, row.youTube, "none", "none", row.secondImage.img.name, row.date, row.user.username, row.season.title])  # Replace field1, field2, field3 with the actual field names of MyClass model
            elif row.fistImage is None and row.secondImage is None and row.pdf is None:                
                # Append row data to the sheet
                sheet.append([row.title, row.content, row.views, row.likes, row.dislikes, row.youTube, "none", "none", "none", row.date, row.user.username, row.season.title])  # Replace field1, field2, field3 with the actual field names of MyClass model
            
            

        # Save the workbook to a buffer
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        
        # Return the Excel file as a HttpResponse
        response = HttpResponse(buffer.getvalue(), content_type='application/vnd.ms-excel')
        if name == '':
            response['Content-Disposition'] = 'attachment; filename=myclass_data.xlsx'  # Provide a filename for the Excel file
        else:
            filename = name+".xlsx"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response

def exportCsv(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        seasonId = request.POST.get('seasonId')        

        if seasonId == 'all':
            myclass_data = post.objects.all()
        else:
            seasons = season.objects.get(id=seasonId)
            myclass_data = post.objects.filter(season=seasons)

        response = HttpResponse(content_type='text/csv')
        if name == '':
            response['Content-Disposition'] = 'attachment; filename="myclass_data.csv"'
        else:
            filename = name+".csv"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
        # Create the CSV writer
        writer = csv.writer(response)
        
        # Write the CSV header row
        writer.writerow(['title', 'content', 'views', 'likes', 'dislikes', 'youTube', 'pdf', 'fistImage', 'secondImage', 'date', 'user.username', 'season',])  # Replace with the actual field names of MyClass model
        
        # Write data to the CSV file
        for row in myclass_data:
            if row.fistImage is not None and row.secondImage is not None and row.pdf is not None:                
                # Append row data to the sheet
                writer.writerow([row.title, row.content, row.views, row.likes, row.dislikes, row.youTube, row.pdf.pdf.name, row.fistImage.img.name, row.secondImage.img.name, row.date, row.user.username, row.season.title])  # Replace field1, field2, field3 with the actual field names of MyClass model
            
            elif row.fistImage is None and row.secondImage is not None and row.pdf is not None:                
                # Append row data to the sheet
                writer.writerow([row.title, row.content, row.views, row.likes, row.dislikes, row.youTube, row.pdf.pdf.name, "none", row.secondImage.img.name, row.date, row.user.username, row.season.title])  # Replace field1, field2, field3 with the actual field names of MyClass model
            elif row.fistImage is not None and row.secondImage is None and row.pdf is not None:                
                # Append row data to the sheet
                writer.writerow([row.title, row.content, row.views, row.likes, row.dislikes, row.youTube, row.pdf.pdf.name, row.fistImage.img.name, "none", row.date, row.user.username, row.season.title])  # Replace field1, field2, field3 with the actual field names of MyClass model
            elif row.fistImage is not None and row.secondImage is not None and row.pdf is None:                
                # Append row data to the sheet
                writer.writerow([row.title, row.content, row.views, row.likes, row.dislikes, row.youTube, "none", row.fistImage.img.name, row.secondImage.img.name, row.date, row.user.username, row.season.title])  # Replace field1, field2, field3 with the actual field names of MyClass model
            
            elif row.fistImage is None and row.secondImage is None and row.pdf is not None:                
                # Append row data to the sheet
                writer.writerow([row.title, row.content, row.views, row.likes, row.dislikes, row.youTube, row.pdf.pdf.name, "none", "none", row.date, row.user.username, row.season.title])  # Replace field1, field2, field3 with the actual field names of MyClass model
            elif row.fistImage is not None and row.secondImage is None and row.pdf is None:                
                # Append row data to the sheet
                writer.writerow([row.title, row.content, row.views, row.likes, row.dislikes, row.youTube, "none", row.fistImage.img.name, "none", row.date, row.user.username, row.season.title])  # Replace field1, field2, field3 with the actual field names of MyClass model
            elif row.fistImage is None and row.secondImage is not None and row.pdf is None:                
                # Append row data to the sheet
                writer.writerow([row.title, row.content, row.views, row.likes, row.dislikes, row.youTube, "none", "none", row.secondImage.img.name, row.date, row.user.username, row.season.title])  # Replace field1, field2, field3 with the actual field names of MyClass model
            elif row.fistImage is None and row.secondImage is None and row.pdf is None:                
                # Append row data to the sheet
                writer.writerow([row.title, row.content, row.views, row.likes, row.dislikes, row.youTube, "none", "none", "none", row.date, row.user.username, row.season.title])  # Replace field1, field2, field3 with the actual field names of MyClass model
            
            
            
        return response

def exportZip(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        seasonId = request.POST.get('seasonId')        

        if seasonId == 'all':
            myclass_data = post.objects.all()
        else:
            seasons = season.objects.get(id=seasonId)
            myclass_data = post.objects.filter(season=seasons)

        response = HttpResponse(content_type='application/zip')
        if name == '':
            response['Content-Disposition'] = 'attachment; filename="myclass_data.zip"'
        else:
            filename = name+".zip"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        # Create a ZIP file
        zip_file = zipfile.ZipFile(response, 'w')
        
        # Iterate over data and add each row as a CSV file to the ZIP file
        for index, row in enumerate(myclass_data):
            # Create a temporary CSV file in memory
            csv_file = HttpResponse(content_type='text/csv')
            csv_file['Content-Disposition'] = f'attachment; filename="myclass_data_{index+1}.csv"'
            
            # Create a CSV writer
            csv_writer = csv.writer(csv_file)
            
            # Write the CSV header row
            csv_writer.writerow(['title', 'content', 'views', 'likes', 'dislikes', 'youTube', 'pdf', 'fistImage', 'secondImage', 'date', 'user.username', 'season'])  # Replace with the actual field names of MyClass model
            
            # Write data to the CSV file
            if row.fistImage is not None and row.secondImage is not None and row.pdf is not None:                
                # Append row data to the sheet
                csv_writer.writerow([row.title, row.content, row.views, row.likes, row.dislikes, row.youTube, row.pdf.pdf.name, row.fistImage.img.name, row.secondImage.img.name, row.date, row.user.username, row.season.title])  # Replace field1, field2, field3 with the actual field names of MyClass model
            
            elif row.fistImage is None and row.secondImage is not None and row.pdf is not None:                
                # Append row data to the sheet
                csv_writer.writerow([row.title, row.content, row.views, row.likes, row.dislikes, row.youTube, row.pdf.pdf.name, "none", row.secondImage.img.name, row.date, row.user.username, row.season.title])  # Replace field1, field2, field3 with the actual field names of MyClass model
            elif row.fistImage is not None and row.secondImage is None and row.pdf is not None:                
                # Append row data to the sheet
                csv_writer.writerow([row.title, row.content, row.views, row.likes, row.dislikes, row.youTube, row.pdf.pdf.name, row.fistImage.img.name, "none", row.date, row.user.username, row.season.title])  # Replace field1, field2, field3 with the actual field names of MyClass model
            elif row.fistImage is not None and row.secondImage is not None and row.pdf is None:                
                # Append row data to the sheet
                csv_writer.writerow([row.title, row.content, row.views, row.likes, row.dislikes, row.youTube, "none", row.fistImage.img.name, row.secondImage.img.name, row.date, row.user.username, row.season.title])  # Replace field1, field2, field3 with the actual field names of MyClass model
            
            elif row.fistImage is None and row.secondImage is None and row.pdf is not None:                
                # Append row data to the sheet
                csv_writer.writerow([row.title, row.content, row.views, row.likes, row.dislikes, row.youTube, row.pdf.pdf.name, "none", "none", row.date, row.user.username, row.season.title])  # Replace field1, field2, field3 with the actual field names of MyClass model
            elif row.fistImage is not None and row.secondImage is None and row.pdf is None:                
                # Append row data to the sheet
                csv_writer.writerow([row.title, row.content, row.views, row.likes, row.dislikes, row.youTube, "none", row.fistImage.img.name, "none", row.date, row.user.username, row.season.title])  # Replace field1, field2, field3 with the actual field names of MyClass model
            elif row.fistImage is None and row.secondImage is not None and row.pdf is None:                
                # Append row data to the sheet
                csv_writer.writerow([row.title, row.content, row.views, row.likes, row.dislikes, row.youTube, "none", "none", row.secondImage.img.name, row.date, row.user.username, row.season.title])  # Replace field1, field2, field3 with the actual field names of MyClass model
            elif row.fistImage is None and row.secondImage is None and row.pdf is None:                
                # Append row data to the sheet
                csv_writer.writerow([row.title, row.content, row.views, row.likes, row.dislikes, row.youTube, "none", "none", "none", row.date, row.user.username, row.season.title])  # Replace field1, field2, field3 with the actual field names of MyClass model
            

            # Add the CSV file to the ZIP file
            zip_file.writestr(f'myclass_data_{index+1}.csv', csv_file.getvalue())
        
        # Close the ZIP file
        zip_file.close()
        
        return response









def error_404(request):
    return render(request, '404.html', {}, status=404)















        









