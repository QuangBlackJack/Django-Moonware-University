import email
from operator import mod
from pickle import FALSE
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from pkg_resources import require


# Create your models here.
# feild
class feild(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name




# model gifs
class gif(models.Model):
    gifLink = models.URLField(max_length=255, default='')

    def __str__(self):
        return self.gifLink








class avatar(models.Model):
    img = models.ImageField(upload_to='static/avatars', null=FALSE, blank=FALSE)

    def __str__(self):
        return self.img.name









# model user info
class userInfo(models.Model):
    email = models.EmailField(max_length=255, unique=True, blank=False)
    password = models.CharField(max_length=255, default='')
    avatar = models.ForeignKey(avatar, on_delete=models.CASCADE)
    PostAmount = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    gif = models.ForeignKey(gif, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, null=True, blank=True)
    feild = models.ForeignKey(feild, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.email

















# model post
class season(models.Model):
    title = models.CharField(max_length=255)
    createDate = models.DateField(null=True)
    firstDeadline = models.DateField()
    secondDeadline = models.DateField()

    def __str__(self):
        return self.title














# img
class firstImg(models.Model):
    img = models.ImageField(upload_to='static/postImgs', null=True, blank=True)

    def __str__(self):
        return self.img.name

class secondImg(models.Model):
    img = models.ImageField(upload_to='static/postImgs', null=True, blank=True)

    def __str__(self):
        return self.img.name

# pdf
class pdf(models.Model):
    pdf = models.FileField(upload_to='static/files', null=True, blank=True)

    def __str__(self):
        return self.pdf.name




# model post
class post(models.Model):
    title = models.CharField(max_length=255, blank=False)
    content = models.TextField(max_length=500, blank=False)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    youTube = models.CharField(max_length=255, null=True, blank=True)
    pdf = models.ForeignKey(pdf, on_delete=models.CASCADE, null=True, blank=True)
    fistImage = models.ForeignKey(firstImg, on_delete=models.CASCADE, null=True, blank=True)
    secondImage = models.ForeignKey(secondImg, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    season = models.ForeignKey(season, on_delete=models.CASCADE, null=True)
    feild = models.ForeignKey(feild, on_delete=models.CASCADE, null=True, blank=True)    

    def __str__(self):
        return self.title


















# views
class view(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username















class like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    like = models.BooleanField(default = False)
    dislike = models.BooleanField(default = False)

    def __str__(self):
        return self.user.username













class comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500, blank=False)

    def __str__(self):
        return self.comment










class report(models.Model):
    report = models.TextField(max_length=500, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField(max_length=255, null=True)
    phone = models.CharField(max_length=20, null=True)













class notification(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(post, on_delete=models.CASCADE, null=True)
    pinned = models.BooleanField(default=False)

    def __str__(self):
        return self.title













class tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name






class tagLink(models.Model):
    tag = models.ForeignKey(tag, on_delete=models.CASCADE)
    post = models.ForeignKey(post, on_delete=models.CASCADE)

    def __str__(self):
        return self.tag.name











