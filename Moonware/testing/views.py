from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import MyImage

def upload_image(request):
    if request.method == 'POST':
        myimage = MyImage(image=request.FILES['image'])
        myimage.save()
        return redirect('success') # redirect to a success page

    return render(request, 'upload_image.html') # render the upload image form


def success(request):
    return HttpResponse("Image uploaded successfully!")
