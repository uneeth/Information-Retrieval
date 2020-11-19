import urllib
import json
from flask import Flask,jsonify
from flask_cors import CORS,cross_origin
from flask import request
import re
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
app = Flask(__name__)
CORS(app,support_credentials=True)
solr = 'http://3.15.158.5:8983'

@app.route('/')
def test():
    return 'Hello'

@app.route('/<query>',methods=['GET','POST'])
def confirmation(query):
    docs=hello_world(query)
    return jsonify(docs)

def clean_tweet(tweet): 
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    
def sentiment_scores(tweet): 
    
    sid_obj = SentimentIntensityAnalyzer()  
    sentiment_dict = sid_obj.polarity_scores(tweet) 
    
    if sentiment_dict['compound'] >= 0.05 : 
        return "Positive" 
  
    elif sentiment_dict['compound'] <= - 0.05 : 
        return "Negative" 
  
    else : 
        return "Neutral"  

def hello_world(query):
    #print(query)
    react_input=[]
    lang_hi='False'
    lang_pt='False'
    lang_en='False'
    topic_pollution=''
    topic_election=''
    topic_corruption=''
    for i in (query.split(",")):
        react_input.append(i)
    print(react_input)
    if(react_input[8]=='false' and react_input[9]=='false' and react_input[10]=='false'):
        topic_pollution=''
        topic_election=''
        topic_corruption=''
    if(react_input[8]=='true'):
        topic_pollution='&tweet_text: pollution'
    if(react_input[9]=='true'):
        topic_election='&tweet_text: election'
    if(react_input[10]=='true'):
        topic_corruption='&tweet_text: corruption'
    if(react_input[5]=='false' and react_input[4]=='false' and react_input[6]=='false'):
        lang_en=''
        lang_pt=''
        lang_hi=''
    if(react_input[5]=='true'):
        lang_en=''
    if(react_input[4]=='true'):
        lang_hi=''
    if(react_input[6]=='true'):
        lang_pt=''
    if(react_input[1]=='false' and react_input[2]=='false' and react_input[3]=='false'):
        country=''
    else:
        country="&fq="+urllib.parse.quote("country: " + ("India" if react_input[1]=='true' else '') + ("&" if (react_input[2]=='true' and react_input[1]=='true') else '') + ("USA" if react_input[2]=='true' else '') + ("&" if( react_input[3]=='true' and react_input[1]=='true') or (react_input[3]=='true' and react_input[2]=='true') else '') + ("Brazil" if react_input[3]=='true' else ''))
    if(react_input[7]=="true"):
        verified="&fq="+urllib.parse.quote("verified:True")
    else:
        verified=''
    query_=react_input[0]
    print(len(query_.split()))
    query = query_.replace(":","")

    URL = solr + "/solr/IRF19P4/select?defType=dismax"+country+verified+"&q="+"tweet_text%3A%20"+urllib.parse.quote(query)+urllib.parse.quote(topic_pollution)+urllib.parse.quote(topic_election)+urllib.parse.quote(topic_corruption)+"&qf=text_en"+urllib.parse.quote(lang_en)+"%20text_hi"+urllib.parse.quote(lang_hi)+"%20text_pt"+urllib.parse.quote(lang_pt)+"&rows=100"
    #data = urllib.request.urlopen(url).read()
    #docs = json.load(str(data))
    #docs = json.dumps(data)
    r = requests.get(url = URL)
    docs = r.json()
    docs = docs['response']['docs']
    print(URL)
    output=[]
    count_en=0
    count_hi=0
    count_pt=0
    count_ot=0
    count_positive=0
    count_negative=0
    count_neutral=0
    count_USA=0
    count_India=0
    count_Brazil=0
    for doc in docs:
        if(doc["country"][0]=="India"):
            count_India+=1
        elif(doc["country"][0]=="USA"):
            count_USA+=1
        else:
            count_Brazil+=1
        if(doc["lang"][0]=="en"):
            count_en+=1
        elif(doc["lang"][0]=="hi"):
            count_hi+=1
        elif(doc["lang"][0]=="pt"):
            count_pt+=1
        else:
            count_ot+=1
        a=str(doc["tweet_text"])
        a=a[2:len(a)-3]
        a=clean_tweet(a)
        a=a.replace('RT @','')
        sentence=sentiment_scores(a)
        if(sentence=='Negative'):
            count_negative+=1
        elif(sentence=="Positive"):
            count_positive+=1
        else:
            count_neutral+=1
    for doc in docs:
        a=str(doc["tweet_text"])
        a=a[2:len(a)-3]
        #print(a)
        a=clean_tweet(a)
        a=a.replace('RT @','')
        sentence=sentiment_scores(a)
        output_temp={}
        z1={'poi_name':doc["poi_name"][0]}
        output_temp.update(z1)
        z2={'tweet_text':doc["tweet_text"][0]}
        output_temp.update(z2)
        z3={'tweet_date':doc["tweet_date"][0]}
        output_temp.update(z3)
        z4={'country':doc["country"][0]}
        output_temp.update(z4)
        z5={'verified':doc["verified"][0]}
        output_temp.update(z5)
        z6={'lang':doc["lang"][0]}
        output_temp.update(z6)
        z7={'sentence':sentence}
        output_temp.update(z7)
        z8={'profile_image_url':doc["user.profile_image_url"][0]}
        output_temp.update(z8)
        z9={'count_en':count_en}
        output_temp.update(z9)
        z10={'count_hi':count_hi}
        output_temp.update(z10)
        z11={'count_pt':count_pt}
        output_temp.update(z11)
        z12={'count_ot':count_ot}
        output_temp.update(z12)
        z13={'count_negative':count_negative}
        output_temp.update(z13)
        z14={'count_positive':count_positive}
        output_temp.update(z14)
        z15={'count_neutral':count_neutral}
        output_temp.update(z15)
        links = re.findall(r"(\w+:\/\/\S+)", doc["tweet_text"][0])
        if(len(links)==0):
            z16={'tweet_url':'https://3.bp.blogspot.com/-FuB1G7ZfEr4/T73fleNd8JI/AAAAAAAAAjs/7iYuFgPPv5s/s1600/smiley-face-flat.jpg'}
        else:
            links = re.findall(r"(\w+:\/\/\S+)", doc["tweet_text"][0])
            z16={"tweet_url":' '.join(map(str, links))}
        output_temp.update(z16)
        z17={'AndrewYang':16.5}
        output_temp.update(z17)
        z18={'JoeBiden':7.22}
        output_temp.update(z18)
        z19={'AmbJohnBolton':2.78}
        output_temp.update(z19)
        z20={'KamalaHarris':8.45}
        output_temp.update(z20)
        z21={'VP':4.62}
        output_temp.update(z21)
        z22={'BolsonaroSP':9.92}
        output_temp.update(z22)
        z23={'cirogomes':3.04}
        output_temp.update(z23)
        z24={'davidmirandario':2.68}
        output_temp.update(z24)
        z25={'dilmabr':2.5}
        output_temp.update(z25)
        z26={'LulaOficial':5.45}
        output_temp.update(z26)
        z27={'yadavakhilesh':1.24}
        output_temp.update(z27)
        z28={'AmitShah':3.53}
        output_temp.update(z28)
        z29={'ArvindKejriwal':2.33}
        output_temp.update(z29)
        z30={'PiyushGoyal':6.52}
        output_temp.update(z30)
        z31={'rajnathsingh':3.1}
        output_temp.update(z31)
        z32={'rsprasad':12.45}
        output_temp.update(z32)
        z33={"tweet_id":doc["id"]}
        output_temp.update(z33)
        z34={"count_USA":count_USA}
        output_temp.update(z34)
        z35={"count_India":count_India}
        output_temp.update(z35)
        z36={"count_Brazil":count_Brazil}
        output_temp.update(z36)
        z37={'Thanking_Government':12.21}
        output_temp.update(z37)
        z38={'Presidential_Elections':14.13}
        output_temp.update(z38)
        z39={'Helath':9.36}
        output_temp.update(z39)
        z40={'Climate_Change':11.29}
        output_temp.update(z40)
        z41={'Vehicle_Act':7.54}
        output_temp.update(z41)
        z42={'Others':35.11}
        output_temp.update(z42)
        z43={'Debate':10.36}
        output_temp.update(z43)
        
        output.append(output_temp)
   # json_output=json.dumps(output)
    return output
  
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)
