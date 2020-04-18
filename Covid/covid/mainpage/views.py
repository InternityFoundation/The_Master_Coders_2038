from django.shortcuts import render

def masterhome(request):
    return render(request,'mainpage/master.html')
def about(request):
    return render(request,'mainpage/about.html')
