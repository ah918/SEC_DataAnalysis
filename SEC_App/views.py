from django.db.models.fields import NullBooleanField
from django.shortcuts import render
from django.http import HttpResponse
from .models import Request

# Create your views here.

def search(request):
    return render(request,'SEC_App/search.html')

def analysis(request):
    keyword = request.POST['keyword']
    period_start = request.POST.get('start_date', None) #"{{placement.date|date:'Y-m-d' }}"
    period_end = request.POST.get('end_date', None) #request.POST['end_date']
    time_start = request.POST.get('strat_time', None)
    time_end = request.POST.get('end_time', None)
    rangeOfsearch = int(request.POST.get('domain', '0'))
    if request.POST['or_and']== 'and':
        includeAll = True
    else:
        includeAll = False

    print(period_start)
    print(rangeOfsearch)
    req = Request(keyword=keyword, period_start=period_start, period_end=period_end, time_start=time_start, time_end=time_end, rangeOfsearch=0, includeAll=includeAll)
    req.save()

    return HttpResponse(keyword)