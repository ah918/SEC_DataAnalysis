from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.json import JSONField

# Create your models here.
class Request(models.Model):
    keyword = models.TextField()
    period_start = models.DateField(null=True)
    period_end = models.DateField(null=True)
    time_start = models.TimeField(null=True)
    time_end = models.TimeField(null=True)
    rangeOfsearch =  models.IntegerField(choices=[(0,'@ALKAHRABA OR @AlkahrabaCare OR كلمة البحث'),(1,'كلمة البحث فقط')])
    date_time = models.DateTimeField()
    includeAll = models.IntegerField(default=0, choices=[(0, "OR"),(1, "AND")])
    
    """
    ----------
    includeAll mean the tweet contains all the keyword 
    ----------
    The rangeOfsearch mean that the serach will include what:
    0 : keyword only
    1 : @Alkahrba or @AlkahrabaCare
    2 : option 1 & 2
    ----------
    """
    
class Tweet(models.Model):
    tweet_id = models.TextField()
    date = models.DateTimeField()
    place = models.TextField()
    tweet_text = models.TextField()
    hashtags =models.TextField()
    urls = models.TextField()
    nlike = models.IntegerField()
    nretweet = models.IntegerField()
    nreply = models.IntegerField()
    username = models.TextField()
    name = models.TextField()
    request = models.ForeignKey(Request, on_delete=CASCADE)
   

class Analysis(models.Model):
    """
    {'tweets_list': tweet_list, 'reactions': reactions, 'req': req, 
    'from_date':from_date, 'to_date':to_date, 'period_data':period_data, 
    'sentiment_data':sentiment_data, 'num_tweets':tweets_df.shape[0], 
    'requests_ids':request.session['requests_ids']}
    """

    request = models.ForeignKey(Request, on_delete=CASCADE)
    tweets_list = models.JSONField()
    dtm = models.JSONField()
    reactions = models.JSONField()
    from_date = models.TextField()
    to_date = models.TextField()
    period_data = models.JSONField()
    sentiment_data = models.JSONField()
    num_tweets = models.IntegerField()
