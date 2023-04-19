from django.contrib import admin
from .models import gif
from .models import userInfo 
from .models import avatar
from .models import post
from .models import season
from .models import view
from .models import like
from .models import comment
from .models import report
from .models import pdf
from .models import firstImg
from .models import secondImg
from .models import notification
from .models import tag, tagLink, feild

# Register your models here.
admin.site.register(gif)
admin.site.register(avatar)
admin.site.register(userInfo)
admin.site.register(post)
admin.site.register(season)
admin.site.register(view)
admin.site.register(like)
admin.site.register(comment)
admin.site.register(report)
admin.site.register(pdf)
admin.site.register(firstImg)
admin.site.register(secondImg)
admin.site.register(notification)
admin.site.register(tag)
admin.site.register(tagLink)
admin.site.register(feild)