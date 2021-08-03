from ast import dump
from re import T
from SEC_App.forms import UserForm
from django.shortcuts import redirect, render
from .models import Analysis, Request
import pandas as pd
from json import dumps, decoder, loads
from django.contrib.auth.decorators import login_required
from .utils import *

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return render(request, 'SEC_App/register.html', {'form': form}) 
    else:
        form = UserForm()
        return render(request, 'SEC_App/register.html', {'form': form})

@login_required
def searchView(request):
    """
    home page / search page
    """
    try:
        req_list = list(Request.objects.filter(user=request.user))
    except:
        req_list = None
    if  req_list != None and len(req_list)>=1:
        return render(request,'SEC_App/search.html', {'query_num': req_list[-1].id})
    else: 
        return render(request,'SEC_App/search.html', {'query_num': None})

@login_required
def analysis(request):
    """
    results and analysis page
    """

    #create request model opject
    req = create_request(request)
    
    #Search for tweets
    try:
        tweets_df = search(req.keyword, limit=request.POST.get('limit',''), 
                            Since = req.period_start, Until = req.period_end)
    except:
        return render(request, 'SEC_App/error.html')

    #save request object
    req.save()
    
    # create and save tweets model objects
    for i, tweet in enumerate(tweets_df):
        req.tweet_set.create(tweet_id=tweets_df.iloc[i].tweet_id, date=tweets_df.iloc[i].date, 
                            place=tweets_df.iloc[i].place, tweet_text=tweets_df.iloc[i].tweet_text, 
                            hashtags=tweets_df.iloc[i].hashtags, urls=tweets_df.iloc[i].urls, 
                            nlike=tweets_df.iloc[i].nlikes, nretweet=tweets_df.iloc[i].nretweets, 
                            nreply=tweets_df.iloc[i].nreplies, username=tweets_df.iloc[i].username, 
                            name=tweets_df.iloc[i].name)
    

    # actual from and to dates
    from_date = tweets_df.iloc[tweets_df.shape[0]-1].date[:10]
    to_date = tweets_df.iloc[0].date[:10]

    req.true_start = from_date
    req.true_end = to_date

    # replace OR & AND with Arabic's for user presentations
    req.presentationkeyword = re.sub('OR','أو',re.sub('AND','و',req.keyword))
    req.save()

    #create requests list object
    try:
        req_list = list(Request.objects.filter(user=request.user))
    except:
        req_list = None

    # *** data preprocessing ***
    #Clean dataframe
    tweets_df_cleaned = cleanDataframe(tweets_df)
    #Clean text
    tweets_df_cleaned_text = tweets_df_cleaned['tweet_text'].apply(lambda text : cleanTxt(text,Emoji_Dict(),stopwords_set()))
    #Preprocessing text: create document term matrix 
    dtm_sentiment = dtm_df(tweets_df_cleaned_text, 'sentiment')
    dtm_topic = dtm_df(tweets_df_cleaned_text, 'topic')
    #(create+show,save:optional) arabic word cloud 
    word_cloud(dtm_topic, path='SEC_App/static/SEC_App/wordcloud.png')

    # *** sentiment and topic predictions ***
    tweets_df_cleaned['sentiment'] = predict_sentiments(dtm_sentiment)
    tweets_df_cleaned['label'] = predict_topic_class(dtm_topic)

    # *** prepare the charts data ****
    reactions = get_reactions_dic(tweets_df_cleaned)
    period_data = get_period_dic(tweets_df_cleaned)
    sentiment_data = get_sentiment_dic(tweets_df_cleaned)
    tweets_dic = get_tweets_dic(tweets_df_cleaned)
    classes_dic = get_classes_dic(tweets_df_cleaned)

    #create analysis object (charts data for faster recreation) 
    req.analysis_set.create(request=req, tweets_list=dumps(tweets_dic), classes_dic=classes_dic, dtm=dtm_topic.to_json(), reactions=reactions, from_date=from_date, 
                            to_date=to_date, period_data=period_data, sentiment_data=sentiment_data, 
                            num_tweets=tweets_df_cleaned.shape[0])

    return render(request, 'SEC_App/results.html',{'tweets_dic': tweets_dic, 'reactions': reactions, 'req': req, 
                                                    'from_date':from_date, 'to_date':to_date, 'period_data':period_data, 
                                                    'sentiment_data':sentiment_data, 'num_tweets':tweets_df_cleaned.shape[0], 
                                                    'req_list':req_list, 'classes_dic': classes_dic})

@login_required
def history(request):
    """
    previous searches/requests page
    """
    #retrieve request model opject
    if request.POST.get('query_num') != None:
        req = Request.objects.get(id=request.POST.get('query_num'))
    else:
        req = Request.objects.get(id=request.GET.get('query_num'))
    
    analysis = Analysis.objects.get(request=req)

    #to decode analysis data
    jsonDec = decoder.JSONDecoder()
    
    #create arabic word cloud 
    word_cloud(pd.read_json(analysis.dtm), path='SEC_App/static/SEC_App/wordcloud.png')

    #create requests list object
    try:
        req_list = list(Request.objects.filter(user=request.user))
    except:
        req_list = None

    return render(request, 'SEC_App/results.html',{'tweets_dic': jsonDec.decode(analysis.tweets_list), 'reactions': analysis.reactions, 'req': req, 
                                                    'from_date':analysis.from_date, 'to_date':analysis.to_date, 'period_data':analysis.period_data, 
                                                    'sentiment_data':analysis.sentiment_data, 'num_tweets':analysis.num_tweets, 
                                                    'req_list':req_list, 'classes_dic': analysis.classes_dic})
