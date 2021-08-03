#Imports 
import pandas as pd
import numpy as np
import pickle
    #For tweet Gathring
import twint
import nest_asyncio
nest_asyncio.apply()
    #For tweet cleaning 
import re
from nltk.tokenize import word_tokenize
from string import punctuation 
import nltk
nltk.download('stop_words')
from nltk.corpus import stopwords 
import string
from pyarabic.araby import *
from pyarabic import trans
    #For tweet Preprocessing 
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
    #For word cloud
from ar_wordcloud import ArabicWordCloud
    #object saving
import joblib
from django.http import HttpResponse


'''___________________________________ STEP1: Data Gathring ____________________________________ '''

def search(keywords , limit, Since = None, Until = None ):
    '''
    [PARAMETERS] 
        Since: 'yyyy-mm-dd' (string)
        Until: 'yyyy-mm-dd' (string)
        keywords: 'word1 OR word2 AND word3' (String)
    [RETURN]
        Tweets_df: (pandas data frame) ['id','date','place','tweet','hashtags','urls','nlikes',
                                        'nretweets','nreplies','username','name','language']]
    '''
    c = twint.Config()
    c.Hide_output = True
    
    #c.Limit = 5 if not (Since or Until) else None
    c.Limit = int(limit) if (limit != "" and limit != None) else 1
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

'''___________________________________ STEP2: Clean dataframe  ____________________________________ '''

def cleanDataframe(Tweets_df):
    '''
    [PARAMETER] 
        Tweets_df: (pandas data frame) ['id','date','place','tweet','hashtags','urls','nlikes',
                                        'nretweets','nreplies','username','name','language'] (pandas.core.frame.DataFrame)

    [RETURN]
        Tweets_df: (pandas data frame) ['id','date','place','tweet','hashtags','urls','nlikes',
                                        'nretweets','nreplies','username','name'] (pandas.core.frame.DataFrame)

    '''
    #convert hashtags and urls data type into list
    df_clean = Tweets_df.copy()
    df_clean.hashtags = df_clean.hashtags.apply(lambda x: " ".join(x))
    df_clean.urls = df_clean.urls.apply(lambda x: " ".join(x))
    #drop duplicates 
    df_clean = df_clean.drop_duplicates(subset=["tweet_text"],keep='first')
    #drop @alkahraba, @alkahrabacare, and @alKahrabaFriend tweets
    df_clean.drop(df_clean[df_clean['username'] == "AlkahrabaCare"].index, inplace = True)
    df_clean.drop(df_clean[df_clean['username'] == "ALKAHRABA"].index, inplace = True) 
    df_clean.drop(df_clean[df_clean['username'] == "alKahrabaFriend"].index, inplace = True)
    #only keep arabic tweets and then drop language column
    df_clean = df_clean.loc[df_clean['language'] == 'ar']
    df_clean = df_clean.drop(['language'], axis=1)
    
    return df_clean


'''___________________________________ STEP3: Clean text  ____________________________________ '''
def Emoji_Dict():
    '''
    [PARAMETERS]:

    [RETURN]:
        Emoji_Dict: {'😞': ':disappointed_face:','😵': ':dizzy_face:',...} (dictionary)
    '''
    with open('SEC_App/static/SEC_App/Emoji_Dict.p', 'rb') as fp:
        Emoji_Dict = pickle.load(fp)
    Emoji_Dict = {v: k for k, v in Emoji_Dict.items()}
    return Emoji_Dict

def convert_emojis_to_word(text,Emoji_Dict):
    '''
    [PARAMETERS]:
        text: text that might have Emojis in it "whay😞??" (string)
        Emoji_Dict: {'😞': ':disappointed_face:','😵': ':dizzy_face:',...} (dictionary)
    [RETURN]:
        text: text with Emojis converted to it corresponding string "whay disappointed_face ??" (string)
    '''
    for emot in Emoji_Dict:
        text = re.sub(r'('+emot+')', ' '+("_".join(Emoji_Dict[emot].replace(",","").replace(":"," ").split()))+' ', text)
    return text

def stopwords_set():
    stopwords_file = open("SEC_App/static/SEC_App/stop_words.txt", "r")
    extra_stopwords = stopwords_file.read()
    extra_stopwords = extra_stopwords.split("\n")
    stopwords_set = set(stopwords.words('arabic')+ extra_stopwords)
    return stopwords_set


def cleanTxt(text,Emoji_Dict,stopwords_set):
    '''
    [PARAMETERS]:
        text: tweet text to be cleaned  (string)
        Emoji_Dict: {'😞': ':disappointed_face:','😵': ':dizzy_face:',...} (dictionary)
        stopwords_set: set of stopwords to be reomved from the text (set)
    [RETURN]:
        text: word tokenized list after text cleaning  ['لمذا','disappointed_face','الكذب'](list of strings)
    '''

    text = text.lower()
    
    text = strip_tatweel(text) #Removing tatweel 
    text = strip_tashkeel(text) #Removing tashkeel
    
    text = re.sub(r'\bال(\w\w+)', r'\1', text)  # Removing al ta3reef
    text = re.sub("[إأآءاٱ]+", "ا", text) # normalize_hamza and unified repeated hamza
    
    text = re.sub('@[A-Za-z0–9]+[\_]*[A-Za-z0–9]*', '', text)  #Removing @mentions
    text = re.sub('[#‘’“”…]', '', text) # Removing '#' hash tag
    text = re.sub('RT[\s]+', '', text) # Removing RT
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', '', text) # Removing URLs
    
    text = re.sub('\[.*&\-]', '', text) #Removing .,*,&,-

    text = re.sub('[%s]' % re.escape(string.punctuation), '', text) #Removing english punctuations
    arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
    text = text.translate(str.maketrans('', '', arabic_punctuations))#Removing arabic punctuations
    
    text = normalize_hamza(text) #normlize hamza آائئء  ---> ءءءءءء
    
    text = trans.normalize_digits(text, source='all', out='west') #arabic (١٢٣٤٥) digits into west(12345)
    text = re.sub('\w*\d\w*', '', text)#Removing digits
    
    text = re.sub(r"\b[a-zA-Z0–9]\b", "", text) #Removing single charcter word
    
    text = convert_emojis_to_word(text,Emoji_Dict)
    text = tokenize(text)

    return [word for word in text if word not in stopwords_set and len(word)>3 ]


'''___________________________________ STEP4: Preprocessing text  ____________________________________ '''

def dtm_df(text_column, task):
    '''
    [PARAMETERS]:
        text_column: dataframe column containing list of word string (pandas.core.series.Series)
    [RETURN]:
        dtm_df: document term matric  (pandas.core.frame.DataFrame)
    '''

    max_df = int(text_column.shape[0]*0.3)
    min_df = int(text_column.shape[0]*0.01)
    
    if task == 'sentiment': # sentiment classfication
        filename = 'sentimentVectorizer.pickle'
    else:                   # topic classification
        filename = 'topicVectorizer.pickle'

    vectorizer = pickle.load(open(filename, 'rb'))
    
    
    text_column = text_column.apply(lambda x : " ".join(x)) # convert column values into string 
    vectorizer_df = vectorizer.transform(text_column)
    dtm_df = pd.DataFrame(vectorizer_df.toarray(), columns=vectorizer.get_feature_names())
    dtm_df.index = text_column.index
    print(dtm_df)
    return dtm_df


'''___________________________________  Word Cloud   ____________________________________ '''

def word_cloud(dtm_df,path = None):
    '''
    [PARAMETERS]:
        dtm_df: document term matric dataframe  (pandas.core.frame.DataFrame)
        path: path where the word cloud to be saved (string)
    [RETURN]:
        awc: arabic word cloud object  (ar_wordcloud.ar_wordcloud.ArabicWordCloud)
    '''   
    awc = ArabicWordCloud(background_color="black",font='NotoSansArabic-ExtraBold.ttf')
    dic_df = {}
    #create dictionary of arabic word with its acurance count
    counter = 0
    for column in dtm_df.columns:
        if not re.search('[a-zA-Z]+',column):
            dic_df[column]= dtm_df[column].sum()
            counter += 1
            if counter >= 50:
                break
    #create word cloud         
    dic_df = awc.from_dict(dic_df, ignore_stopwords=True)
    #show word cloud
    #awc.plot(dic_df, title="سحابة الكلمات ", width=8, height=7)
    #save word cloud 
    if path:
        awc.to_file(path)

'''___________________________________  Predict Sentiments & Topic Class  ____________________________________ '''

def predict_sentiments(dtm):
    
    filename = 'sentimentModel.sav'
    # load the model from disk
    loaded_model = joblib.load(filename)
    result = loaded_model.predict(dtm)
    
    return result

def predict_topic_class(dtm):
    
    # load the model from disk
    topic_model = joblib.load('topicModel.sav')
    results = topic_model.predict(dtm)
    return results

'''___________________________________ Views Helper Functions  ____________________________________ '''

from django.contrib.auth.models import User
from .models import Request
from django.utils import timezone
import datetime
from json import dumps, decoder, loads

def get_reactions_dic(tweets_df):
    '''
    Create dictionary that summarize reactions [likes, tweets, replies] numbers for each sentiment [negative, neutral, positive]
    
    return: json rections dictionary {
                                        'likes': int[negative, neutral, positive],
                                        'replies': int[negative, neutral, positive],
                                        'retweets': int[negative, neutral, positive]
                                     }
    '''
    
    tweets_df_reactions = pd.DataFrame()
    tweets_df_reactions['nlikes']= tweets_df['nlikes']
    tweets_df_reactions['nretweets'] = tweets_df['nretweets']
    tweets_df_reactions['nreplies'] = tweets_df['nreplies']
    tweets_df_reactions['sentiment'] = tweets_df['sentiment']
    tweets_df_reactions_negative = pd.DataFrame(tweets_df_reactions[tweets_df_reactions['sentiment']=='-1'])
    tweets_df_reactions_neutral = pd.DataFrame(tweets_df_reactions[tweets_df_reactions['sentiment']=='0'])
    tweets_df_reactions_positive = pd.DataFrame(tweets_df_reactions[tweets_df_reactions['sentiment']=='1'])

    likes_list = [int(np.sum(tweets_df_reactions_negative['nlikes'])), int(np.sum(tweets_df_reactions_neutral['nlikes'])), int(np.sum(tweets_df_reactions_positive['nlikes'])) ]
    replies_list = [int(np.sum(tweets_df_reactions_negative['nreplies'])), int(np.sum(tweets_df_reactions_neutral['nreplies'])), int(np.sum(tweets_df_reactions_positive['nreplies'])) ]
    retweets_list = [int(np.sum(tweets_df_reactions_negative['nretweets'])), int(np.sum(tweets_df_reactions_neutral['nretweets'])), int(np.sum(tweets_df_reactions_positive['nretweets'])) ]

    reactions_dic = {
        'likes': likes_list,
        'replies': replies_list,
        'retweets': retweets_list
    }

    # convert to json
    reactions = dumps(reactions_dic)

    return reactions

def get_period_dic(tweets_df):
    '''
    Create dictionary that summarize number of tweets in three periods [hours, days, months] for each sentiment.
    
    return: json periods dictionary {
                                        'negativeDays': [int],
                                        'neutralDays': [int],
                                        'positiveDays': [int],
                                        'negativeMonths': [int],
                                        'neutralMonths': [int],
                                        'positiveMonths': [int],
                                        'negativeHours': [int],
                                        'neutralHours': [int],
                                        'positiveHours': [int]
                                    }
    '''
    periods_df = tweets_df
    tweets_df_negative = pd.DataFrame(periods_df[periods_df['sentiment']=='-1'])
    tweets_df_neutral = pd.DataFrame(periods_df[periods_df['sentiment']=='0'])
    tweets_df_positive = pd.DataFrame(periods_df[periods_df['sentiment']=='1'])
    ########
    tweets_df_negative_Day_List = getListDays(tweets_df_negative)
    tweets_df_neutral_Day_List = getListDays(tweets_df_neutral)
    tweets_df_positive_Day_List = getListDays(tweets_df_positive)
    tweets_df_negative_Months_List = getListMonths(tweets_df_negative)
    tweets_df_neutral_Months_List = getListMonths(tweets_df_neutral)
    tweets_df_positive_Months_List = getListMonths(tweets_df_positive)
    tweets_df_negative_Hours_List = getListHours(tweets_df_negative)
    tweets_df_neutral_Hours_List = getListHours(tweets_df_neutral)
    tweets_df_positive_Hours_List = getListHours(tweets_df_positive)
   
    periods_dic = {
        'negativeDays': tweets_df_negative_Day_List,
        'neutralDays': tweets_df_neutral_Day_List,
        'positiveDays': tweets_df_positive_Day_List,
        'negativeMonths': tweets_df_negative_Months_List,
        'neutralMonths': tweets_df_neutral_Months_List,
        'positiveMonths': tweets_df_positive_Months_List,
        'negativeHours': tweets_df_negative_Hours_List,
        'neutralHours': tweets_df_neutral_Hours_List,
        'positiveHours': tweets_df_positive_Hours_List
    }

    # convert to json
    periods = dumps(periods_dic)

    return periods

def getListDays(tweets_df_sen):
    '''
    count the number of tweets in each day in the recieved dataframe
    return: list of length 7, contains counts of tweets in each day from Saturday to Sunday 
    '''
    Full_Date = tweets_df_sen['date'].values.tolist()
    z=0
    newDay = []
    for i in Full_Date:
          e = Full_Date[z]
          date= e[0:10]
          day_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
          day = datetime.datetime.strptime(date,'%Y-%m-%d').weekday()
          newDay.append(day_name[day])
          z=z+1
   
    days = [newDay.count("Saturday"),newDay.count("Friday"),newDay.count("Thursday"),newDay.count("Wednesday"),newDay.count("Tuesday"),newDay.count("Monday"),newDay.count("Sunday")]
    return days
    
def getListMonths(tweets_df_sen):
    '''
    count the number of tweets in each month in the recieved dataframe
    return: list of length 12, contains counts of tweets in each month from December to January
    '''
    Full_Date = tweets_df_sen['date'].values.tolist()
    z=0
    newMon = []
    for i in Full_Date:
          e = Full_Date[z]
          mon= e[5:7]
          newMon.append(mon)
          z=z+1
    months= [newMon.count("12"),newMon.count("11"),newMon.count("10"),newMon.count("09"),newMon.count("08"),newMon.count("07"),newMon.count("06"),newMon.count("05"),newMon.count("04"),newMon.count("03"),newMon.count("02"),newMon.count("01")]      
    return months

def getListHours(tweets_df_sen):
    '''
    count the number of tweets in each hour in the recieved dataframe
    return: list of length 24, contains counts of tweets in each hour from 00 to 24 
    '''
    Full_Date = tweets_df_sen['date'].values.tolist()
    z=0
    newH = []
    for i in Full_Date:
          e = Full_Date[z]
          mon= e[11:13]
          newH.append(mon)
          z=z+1
    Hours= [newH.count("00"),newH.count("01"),newH.count("02"),newH.count("03"),newH.count("04"),newH.count("05"),newH.count("06"),newH.count("07"),newH.count("08"),newH.count("09"),newH.count("10"),newH.count("11"),newH.count("12"),newH.count("13"),newH.count("14"),newH.count("15"),newH.count("16"),newH.count("17"),newH.count("18"),newH.count("19"),newH.count("20"),newH.count("21"),newH.count("22"),newH.count("23")]      
    return Hours

def get_sentiment_dic(tweets_df):
    '''
    Create dictionary that count the number of tweets with each sentiment(positive, negative, neutral)
    
    return: json sentiment dictionary {
                                        'sentiment': int[positive, negative, neutral]
                                       }
    '''

    sentiment_df = pd.DataFrame()
    sentiment_df['sentiment'] = tweets_df['sentiment']
    sentiment_dic = {
        'sentiment': [tweets_df[tweets_df['sentiment']=='1'].shape[0], tweets_df[tweets_df['sentiment']=='-1'].shape[0], tweets_df[tweets_df['sentiment']=='0'].shape[0]] 
    }
    return dumps(sentiment_dic)

def get_tweets_dic(tweets_df_cleaned):
    '''
    Create dictionary of lists of tweets' text
    
    return: json tweets text lists dictionary {
                                            'all_tweets': [str],
                                            'neutral_tweets': [str],
                                            'positive_tweets': [str],
                                            'negative_tweets': [str]
                                        }
    '''
    map = {
        '1': 'انقطاع',
        '2': 'خطر',
        '3': 'فاتورة',
        '4': 'أخرى'
    }

    tweets_df_classes = tweets_df_cleaned[['tweet_text', 'label']]
    tweets_df_classes['label'] = tweets_df_classes['label'].map(map)
    tweet_list = tweets_df_classes.values.tolist()
    neutral_tweets = tweets_df_classes[tweets_df_cleaned['sentiment']=='0'].values.tolist()
    positive_tweets = tweets_df_classes[tweets_df_cleaned['sentiment']=='1'].values.tolist()
    negative_tweets = tweets_df_classes[tweets_df_cleaned['sentiment']=='-1'].values.tolist()

    tweets_dic = {
        'all_tweets': tweet_list,
        'neutral_tweets': neutral_tweets,
        'positive_tweets': positive_tweets,
        'negative_tweets': negative_tweets
    }

    return tweets_dic

def get_classes_dic(tweets_df_cleaned):
    '''
    Create dictionary of number of tweets in each topic class
    
    return: json topic dictionary {
                                    'interuption': int,
                                    'risk': int,
                                    'bill': int,
                                    'others': int
                                  }
    '''
    interuption = tweets_df_cleaned[tweets_df_cleaned['label']=='1'].shape[0]
    risk = tweets_df_cleaned[tweets_df_cleaned['label']=='2'].shape[0]
    bill = tweets_df_cleaned[tweets_df_cleaned['label']=='3'].shape[0]
    other = tweets_df_cleaned[tweets_df_cleaned['label']=='4'].shape[0]

    classes_dic = {
        'interuption': interuption,
        'risk': risk,
        'bill': bill,
        'others': other
    }
    
    return dumps(classes_dic)

def create_request(request):
    '''
    Take http request of the user search request
    return: request model object (user tweets collection request)
    '''
    includeAll = request.POST['or_and']
    rangeOfsearch = request.POST.get('domain', 0)
    keyword = request.POST['keyword']
    time_start = request.POST.get('start_time', None) if request.POST.get('start_time', None) != "" else None
    time_end = request.POST.get('end_time', None) if request.POST.get('end_time', None) != "" else None
    rangeOfsearch = request.POST.get('domain', 0)
    date_time =  timezone.now()

    # Generate a complete keyword
    if len(keyword)==0:
        keyword = "@ALKAHRABA OR @AlkahrabaCare"
    else:
        keywords_list = keyword.split(' ')
        if rangeOfsearch == "0":
            print("i am inside rangeOfsearch == 0")
            if len(keywords_list)<=1:
                keyword = "(@ALKAHRABA OR @AlkahrabaCare) AND " + keyword
                print("i am inside len(keywords_list)<=1", keywords_list)
            elif includeAll == '1':
                print("i am inside and and", keywords_list)
                keyword = "(@ALKAHRABA OR @AlkahrabaCare) AND "+' AND '.join(keywords_list)
            else:
                print("i am inside or or", keywords_list)
                keyword = "(@ALKAHRABA OR @AlkahrabaCare AND) "+' OR '.join(keywords_list)
        elif len(keywords_list)==1:
            keyword = keyword
        elif includeAll == '1':
            keyword = ' AND '.join(keywords_list)
        else:
            keyword = ' OR '.join(keywords_list) 
    
    # Verify and automatically correct dates
    period_start = request.POST.get('period_start', None) if request.POST.get('period_start', None) != "" else None #"{{placement.date|date:'Y-m-d' }}"
    if period_start != None: 
        period_start = period_start[6:] + "-" + period_start[:2] + "-" + period_start[3:5]
        period_start_date = datetime.date(int(period_start[0:4]),int(period_start[5:7]),int(period_start[8:]))
        if period_start_date > timezone.now().date():
            period_start = None  

    period_end = request.POST.get('end_period', None)  if request.POST.get('end_period', None) != "" else None
    if period_end != None:
        period_end = period_end[6:] + "-" + period_end[:2] + "-" + period_end[3:5]
        period_end_date = datetime.date(int(period_end[0:4]),int(period_end[5:7]),int(period_end[8:]))
        if (period_start != None and period_end_date  < period_start_date) or period_end_date > timezone.now().date():
            period_end = str(timezone.now().date())

    #creat request opject
    req = Request(user=request.user, keyword=keyword, period_start=period_start, period_end=period_end, time_start=time_start, time_end=time_end, rangeOfsearch=rangeOfsearch, date_time=date_time, includeAll=includeAll)

    return req
