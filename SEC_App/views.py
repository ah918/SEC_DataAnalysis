from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def search(request):
    return render(request,'SEC_APP/search.html')