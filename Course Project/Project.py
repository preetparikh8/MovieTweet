import twitter
import sys
import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
import pattern.en
from sklearn.cluster import KMeans
import numpy
import matplotlib.mlab as mlab

reload(sys)
sys.setdefaultencoding("utf-8")


api=twitter.Api(consumer_key='fWgdytSVKGu4jaB3hyAoFN45w',
                  consumer_secret='UMwQ4IPO8H1DMXFmGo8hDq8obmwvKNdhiVZGHSr62z1to7SInO',
                  access_token_key='1339518248-WA5LD7c1EYej6qUIJLecM0LBRQP9nTVcshzmWqo',
                  access_token_secret='oO7AwxNR3kKiZCYigpiaIUHafsjiPe9I0QJSk5PB7IyF6')

movie=raw_input("Movie name: ")

directory=movie

try:
    if not os.path.exists(directory):
        os.makedirs(directory)
except OSError:
        print ('Error: Creating directory. ' +  directory)


def query_ex1():
    query = movie+' AND movie AND review'
    MAX_ID = None
    tweets = api.GetSearch(query,count=100, max_id=MAX_ID, result_type='mixed')
    for raw_tweet in tweets:
        tweet = json.loads(str(raw_tweet))
        #info = {"created_at": tweet['created_at'],"screen_name": tweet['user'], "text": tweet['text']}
        info={"text":tweet['text']}
        f=open(""+movie+"/"+movie+".txt", 'a+')
        f.write(json.dumps(str(info)))
        f.write("\n")
        f.close()

    print "Tweets Collected and saved in file"

print query_ex1()

#Sentiment Analysis
c=0
f=open(""+movie+"/"+movie+".txt").readlines()
b=sum(1 for line in f)
for line in f:
#print pattern.en.sentiment(line)
    a=pattern.en.polarity(line)
    e=a
    c=c+e
d=c/b
print "polarity",d
if d==1:
    print "User rating: 5"
elif d<1 and d>=0.5:
    print "User rating: 4.5"
elif d<0.5 and d>0.3:
    print "User rating: 4"
elif d<=0.3 and d>0:
    print "User rating: 3"
elif d>-0.5 and d<=0:
    print "User rating: 2"
elif d<-0.5 and d>=-1:
    print "User rating: 1"
else:
    print "User rating: 0"


def piechart():
    tweets1=[]
    pos = 0
    neg=0
    nut=0
    f=open(""+movie+"/"+movie+".txt").readlines()
    c = sum(1 for line in f)
    print "total numbers of tweets",c

    for line in f:
        a = pattern.en.polarity(line)
        if a > 0 and a <= 1:
            pos = pos + 1
    print "Positive tweets: ", pos

    for line1 in f:
        a = pattern.en.polarity(line1)
        if a < 0 and a >= -1:
            neg = neg + 1
    print "Negative tweets: ", neg

    for line2 in f:
        a = pattern.en.polarity(line2)
        if a == 0:
            nut = nut + 1
    print "Neutral tweets: ", nut

    labels = 'Positive tweets', 'Negative tweets', 'Neutral tweets'
    sizes=[pos,neg,nut]
    colors=['red','lightgreen','skyblue']
    explode=(0.1,0,0)
    plt.title(movie)
    plt.pie(sizes,explode=explode,labels=labels,colors=colors,autopct='%1.1f%%',shadow=True,startangle=140)
    plt.show()

print piechart()

stopwords = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the", "Movie", "https co"]


#Wordcloud
def wordc():
    tweets=open(""+movie+"/"+movie+".txt").read()
    term = tweets.split(" ")
    if term not in stopwords:
        word_cloud = WordCloud(stopwords= "movie review" ,max_font_size=50).generate(tweets)
        plt.figure()
        plt.imshow(word_cloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()

print wordc()
print "WordCloud Created!!"

tweets = []
for line in open(""+movie+"/"+movie+".txt").readlines():
    tweets.append(line)

# Extract the vocabulary of keywords
vocab = dict()
for text in tweets:
    for term in text.split():
        term = term.lower()
        if len(term) > 2 and term not in stopwords:
            if vocab.has_key(term):
                vocab[term] = vocab[term] + 1
            else:
                vocab[term] = 1

# Remove terms whose frequencies are less than a threshold (e.g., 15)
vocab = {term: freq for term, freq in vocab.items() if freq > 25}
# Generate an id (starting from 0) for each term in vocab
vocab = {term: idx for idx, (term, freq) in enumerate(vocab.items())}

# Generate X
X = []
for text in tweets:
    x = [0] * len(vocab)
    terms = [term for term in text.split() if len(term) > 2]
    for term in terms:
        if vocab.has_key(term):
            x[vocab[term]] += 1
    X.append(x)

# K-means clustering
km = KMeans(n_clusters = 5, n_init = 100) # try 100 different initial centroids
km.fit(X)

cluster = []
# Print tweets that belong to cluster 2
for idx, cls in enumerate(km.labels_):
    if cls == 0:
        cluster.append(tweets[idx])
        f=open(""+movie+"/Cluster1.txt",'a')
        f.write(tweets[idx])
    elif cls == 1:
        cluster.append(tweets[idx])
        f = open(""+movie+"/Cluster2.txt", 'a')
        f.write(tweets[idx])
    elif cls == 2:
        cluster.append(tweets[idx])
        f = open(""+movie+"/Cluster3.txt", 'a')
        f.write(tweets[idx])
print "Clusters created!"
