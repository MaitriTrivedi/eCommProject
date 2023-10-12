from django.shortcuts import render

# Create your views here.
def folders(request):
    return render(request,'folders/folders.html')