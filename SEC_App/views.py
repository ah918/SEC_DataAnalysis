from django.http.response import HttpResponseRedirect
from SEC_App.forms import RequestForm
from django.shortcuts import render
from django.http import HttpResponse
from .models import Request, Tweet
from django.utils import timezone
import pandas as pd
import datetime

import twint
import nest_asyncio
nest_asyncio.apply()
# Create your views here.


def twitter_search(keywords , Since = None, Until = None ):
    c = twint.Config()
    c.Hide_output = True
    c.Limit = 10_000 #if not (Since or Until) else None
    #PANDAS
    c.Pandas = True
    c.Pandas_au = True
    c.Pandas_clean = True
    #SEARCH
    c.Search = keywords
    c.Since = Since
    c.Until = Until
    twint.run.Search(c)
    Tweets_df = twint.storage.panda.Tweets_df[['id','date','place','tweet','hashtags','urls',
                                            'nlikes','nretweets','nreplies','username','name','language']]
    Tweets_df.rename({'id': 'tweet_id', 'tweet': 'tweet_text'}, axis=1, inplace=True)
    return Tweets_df

def search(request):
    # if request.method == 'POST':
    #     # create a form instance and populate it with data from the request:
    #     form = RequestForm(request.POST)
    #     form.save()
    #     return HttpResponseRedirect(request, "done")
    
    # form = RequestForm()
    # return render(request,'SEC_App/requestform.html', {'form': form})
    return render(request,'SEC_App/search.html')

def analysis(request):
    
    
    includeAll = request.POST['or_and']
    rangeOfsearch = request.POST.get('domain', 0)

    keyword = request.POST['keyword']
    
    if len(keyword)==0:
        keyword = "@ALKAHRABA OR @AlkahrabaCare"
    else:
        keywords_list = ' '.split(keyword)

        if rangeOfsearch == 0:
            if len(keywords_list)<=1:
                keyword = "@ALKAHRABA OR @AlkahrabaCare OR" + keyword
            elif includeAll:
                keyword = "(@ALKAHRABA OR @AlkahrabaCare) AND"+' AND '.join(keywords_list)
            else:
                keyword = "@ALKAHRABA OR @AlkahrabaCare OR"+' OR '.join(keywords_list)
        elif len(keywords_list)==1:
            keyword = keyword
        elif not includeAll:
            keyword = ' AND '.join(keywords_list)
        else:
            keyword = ' OR '.join(keywords_list) 
    
    period_start = request.POST.get('period_start', None) if request.POST.get('period_start', None) != "" else None #"{{placement.date|date:'Y-m-d' }}"
    if period_start != None: 
        period_start = period_start[6:] + "-" + period_start[:2] + "-" + period_start[3:5]
        period_start_date = datetime.date(int(period_start[0:3]),int(period_start[5:6]),int(period_start[8:]))
    if period_start_date > timezone.now().date():
        period_start = None  

    period_end = request.POST.get('end_period', None)  if request.POST.get('end_period', None) != "" else None
    if period_end != None:
        if (period_start != None and period_end < period_start) or period_end > timezone.now().date():
            period_end = timezone.now().date()
        else:
            period_end = period_end[6:] + "-" + period_end[:2] + "-" + period_end[3:5]

    time_start = request.POST.get('start_time', None) if request.POST.get('start_time', None) != "" else None
    time_end = request.POST.get('end_time', None) if request.POST.get('end_time', None) != "" else None
    rangeOfsearch = request.POST.get('domain', 0)
    date_time =  timezone.now()
    
    print(period_start)
    print(period_end)
    print(rangeOfsearch)
    req = Request(keyword=keyword, period_start=period_start, period_end=period_end, time_start=time_start, time_end=time_end, rangeOfsearch=rangeOfsearch, date_time=date_time, includeAll=includeAll)
    req.save()

    tweets_df = twitter_search(keyword, Since = period_start, Until = period_end)
    print(tweets_df.size)
    for i, tweet in enumerate(tweets_df):
        req.tweet_set.create(tweet_id=tweets_df.iloc[i].tweet_id, date=tweets_df.iloc[i].date, place=tweets_df.iloc[i].place, tweet_text=tweets_df.iloc[i].tweet_text, hashtags=tweets_df.iloc[i].hashtags, urls=tweets_df.iloc[i].urls, nlike=tweets_df.iloc[i].nlikes, nretweet=tweets_df.iloc[i].nretweets, nreply=tweets_df.iloc[i].nreplies, username=tweets_df.iloc[i].username, name=tweets_df.iloc[i].name)
    req.save()

    tweet_list = tweets_df.head(50)['tweet_text'].to_list()
    tweets_list = '\n'.join(tweet_list)
    
    return render(request, 'SEC_App/results.html',{'tweets_list': tweet_list})

