from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.json import JSONField
from django.conf import settings
import re

# Create your models here.
class Request(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    keyword = models.TextField()
    presentationkeyword = models.TextField(null=True, default=None)
    period_start = models.DateField(null=True)
    period_end = models.DateField(null=True)
    true_start = models.TextField(null=True)
    true_end = models.TextField(null=True)
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
    period-start, period_end: specified by the user
    true_start, true_end: from the extracted tweets 
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
    request = models.ForeignKey(Request, on_delete=CASCADE)
    tweets_list = models.JSONField()
    dtm = models.JSONField()
    reactions = models.JSONField()
    from_date = models.TextField()
    to_date = models.TextField()
    period_data = models.JSONField()
    sentiment_data = models.JSONField()
    num_tweets = models.IntegerField()
