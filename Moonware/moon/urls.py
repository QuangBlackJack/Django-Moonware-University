from django.urls import URLPattern, path
from . import views

urlpatterns = [
    # landing page & some common functions
    path('', views.index, name='index'),
    path('aboutUs/', views.aboutUs, name='aboutUs'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.user_register, name='register'),
    path('activate/', views.activate, name="activate"),
    path('checkOtpToLogin/', views.checkOtpToLogin, name="checkOtpToLogin"),

    # forgot password
    path('forgotPassword/', views.forgotPassword, name="forgotPassword"),
    path('checkOtp/', views.checkOtp, name="checkOtp"),
    path('newPass/', views.newPass, name="newPass"),
    path('passChanged/', views.passChanged, name="passChanged"),

    # change pass regular (still remember pass)
    path('otpToChangePass/', views.otpToChangePass, name="otpToChangePass"),
    path('checkOtpToPassword/', views.checkOtpToPassword, name="checkOtpToPassword"),
    path('finallyChangePass/', views.finallyChangePass, name="finallyChangePass"),

    # bullshit functions
    path('updateGif/<int:pk>/', views.updateGif, name='updateGif'),
    path('updateAvatar/<int:pk>/', views.updateAvatar, name="updateAvatar"),
    path('notificate/', views.notificate, name="notificate"),
    path('pinNotificate/<int:pk>/', views.pinNotificate, name="pinNotificate"),
    path('unPinNotificate/<int:pk>/', views.unPinNotificate, name="unPinNotificate"),
    path('deleteNotification/<int:pk>/', views.deleteNotification, name="deleteNotification"),
    
    # user managements and actions
    path('account/', views.account, name="account"),    
    path('storage/', views.storage, name="storage"),
    path('createPost/', views.createPost, name="createPost"),
    path('updatePost/', views.updatePost, name="updatePost"),
    path('postDetail/<int:pk>/', views.postDetail, name='postDetail'),
    path('likeOrDislike/', views.likeOrDislike, name='likeOrDislike'),
    path('createComment/', views.createComment, name='createComment'),
    path('deletePost/', views.deletePost, name='deletePost'),
    path('showByTag/<int:pk>/', views.showByTag, name='showByTag'),
    path('addTags/<int:pk>/', views.addTags, name='addTags'),
    path('addTagsFinal/', views.addTagsFinal, name='addTagsFinal'),
    path('deleteTag/', views.deleteTag, name='deleteTag'),


    # still cant remember wtf is this shit
    path('loginToChangePass/', views.loginToChangePass, name="loginToChangePass"),
    
    
    
    
    
    # simplely, just a log out
    path('logout/', views.user_logout, name='logout'),



    # export
    path('exportData/', views.exportData, name='exportData'),
    path('exportExcel/', views.exportExcel, name='exportExcel'),
    path('exportCsv/', views.exportCsv, name='exportCsv'),
    path('exportZip/', views.exportZip, name='exportZip'),
    
]
