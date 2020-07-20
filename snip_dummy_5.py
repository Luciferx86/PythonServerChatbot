from flask import Flask,request, render_template
import urllib.request as requests
import json
import os
from snips_nlu import SnipsNLUEngine
import io
import random
import json
import dateutil.parser
from fuzzywuzzy import process
from snips_nlu import SnipsNLUEngine, load_resources
from snips_nlu.default_configs import CONFIG_EN
from snips_nlu_parsers import BuiltinEntityParser
import json
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import sqlite3
from pprint import pprint
from jsonmerge import merge
import os
from datetime import date
account_sid = 'AC35411e153787c8eb91d4f0a62603992d'
auth_token = '8d032fd786abec43da644368fc034de6'
client = Client(account_sid, auth_token)

default_engine = SnipsNLUEngine()

list_doc = ["doctor rekha pradeep", "doctor arvind shenoi", "doctor ashwin", "doctor ajay", "doctor urvashi", "doctor kanjus", "doctor akshay", "doctor sahu"]

def init_snipsnlu():
        # engine = SnipsNLUEngine(config=CONFIG_EN)
        engine = SnipsNLUEngine(resources=load_resources("snips_nlu_en"))
        with io.open("proj.json") as f:
            dataset = json.load(f)
            engine.fit(dataset)
        return engine

snips_nlu_engine = init_snipsnlu()

def response(utterances, userID='123', show_details=False):
        print(utterances)
        context = {}
        seed = 42                                                                                                                                                                                            
        engine = snips_nlu_engine
        parser = BuiltinEntityParser.build(language="en")
        user_input = json.loads(utterances)
        print(user_input)
        samp = {}
        for key,value in user_input.items():
            if key!= 'text': 
               samp.update({key:value}) 
        parsing = engine.parse(user_input['text'])    
        doc = json.loads(json.dumps(parsing))
        print(doc)
        intent = doc['intent']
        print(intent) 
        if not doc['slots']:
             resp = 'Sorry,I do not get you, Please say it again!'
             full_response = {'Date':None,'Time':None,'Doctor Name':None,'text':str(resp)}
             return json.dumps(full_response)
        name = ""
        for res in doc['slots']:
            if res['entity'] == 'doc':
                 name = res['rawValue'] 
                 name1= process.extractOne(name,list_doc)
                 print(name1)
                 if name1[1] < 68:	
                      print(name1[0])
                      full_response = {'text':'Sorry,the doctor by this name does not exist,So please say the correct doctor name'}
                      samp.update(full_response)
                      print(samp)
                      return json.dumps(samp)
                 else:
                      Doctors_Name = name1[0]
                
                    
                    
        intent = doc['intent']
        Intent = intent['intentName']
    
    
                    
        if (Intent == 'doctor_day_time'):
            u1 = json.loads(utterances)
            parsing1 = parser.parse(u1['text'])
            date = json.loads(json.dumps(parsing1))
            count = len(date) 
            if count == 1:
                 date_time = date[0]['entity']['value']       
                 d = dateutil.parser.parse(date_time).date()
                 d1 = dateutil.parser.parse(date_time).time()
            else:
                 date_time = date[0]['entity']['value']
                 date_time1 = date[1]['entity']['value']
                 if date[1]['entity']['grain'] == 'Hour':
                     d = dateutil.parser.parse(date_time).date()
                     d1 = dateutil.parser.parse(date_time1).time()
                 else:
                     d = dateutil.parser.parse(date_time1).date()
                     d1 = dateutil.parser.parse(date_time).time()
            full_response = {'Date':str(d),'Time':str(d1),'Doctor Name':str(Doctors_Name)}
            dictionary = {'Date':str(d),'Time':str(d1),'Doctor Name':str(Doctors_Name)}

        elif (Intent == 'doctor_day'):
            u1 = json.loads(utterances)
            print(u1['text'])
            parsing1 = parser.parse(u1['text'])
            date = json.loads(json.dumps(parsing1))
            date_time = date[0]['entity']['value']
            d = dateutil.parser.parse(date_time).date()
            full_response = {'Date':str(d),'Time':None,'Doctor Name':str(Doctors_Name)}
            dictionary = {'Date':str(d), 'Doctor Name':str(Doctors_Name)}        
        elif (Intent == 'doctor'):
            full_response = {'Date':None,'Time':None,'Doctor Name':str(Doctors_Name)}
            dictionary = {'Doctor Name':str(Doctors_Name)}
            
        elif(Intent == 'time'):
            u1 = json.loads(utterances)
            print(u1['text'])
            parsing1 = parser.parse(u1['text'])
            date = json.loads(json.dumps(parsing1))
            date_time = date[0]['entity']['value']
            d1 = dateutil.parser.parse(date_time).time()
            full_response = {'Date':None,'Time':str(d1),'Doctor Name':None}
            dictionary = {'Time':str(d1)}
        elif(Intent == 'day'):
            u1 = json.loads(utterances)
            print(u1['text'])
            parsing1 = parser.parse(u1['text'])
            date = json.loads(json.dumps(parsing1))
            date_time = date[0]['entity']['value']
            d = dateutil.parser.parse(date_time).date()
            full_response = {'Date':str(d),'Time':None,'Doctor Name':None}
            dictionary = {'Date':str(d)}
        elif(Intent == 'day_time'):
            u1 = json.loads(utterances)
            print(u1['text'])
            parsing1 = parser.parse(u1['text'])
            date = json.loads(json.dumps(parsing1))
            date_time = date[0]['entity']['value']
            d = dateutil.parser.parse(date_time).date()
            d1 = dateutil.parser.parse(date_time).time()
            full_response ={'Date':str(d),'Time':str(d1),'Doctor Name':None}
            dictionary = {'Date':str(d),'Time':str(d1)}
        elif (Intent == 'doctor_time'):
            u1 = json.loads(utterances)
            print(u1['text'])
            parsing1 = parser.parse(u1['text'])
            date = json.loads(json.dumps(parsing1))
            date_time = date[0]['entity']['value']
            d1 = dateutil.parser.parse(date_time).time()
            full_response = {'Date':None,'Time':str(d1),'Doctor Name':str(Doctors_Name)}
            dictionary = {'Time':str(d1),'Doctor Name':str(Doctors_Name)}
            
        else:
            full_response = {'Date':None,'Time':None,'Doctor Name':None} 
            dictionary = {'Date':None,'Time':None,'Doctor Name':None} 
            with open('./proj_reply.json') as json_data:
                 intents = json.load(json_data)
            if intent:
                  while intent:
                    for i in intents['intents']:
                        print(i,Intent)
                        if i['tag'] == Intent:
                            if 'context_set' in i:
                                if show_details: print ('context:', i['contexit_set'])
                                context[userID] = i['context_set']

                            if not 'context_filter' in i or \
                                (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                                if show_details: print ('tag:', i['tag'])
                                full_response.update( {"text":str(random.choice(i['responses']))} )
                                return json.dumps(full_response)
                    Intent.pop(0) 
                
        print('******************************')
        
        print(dictionary)
        
        new_dict = json.dumps(dictionary)
       
        f = open("dict.txt","a")
        resaa = f.write(new_dict)
        f.close()
 
        
        file = open("dict.txt","r")
        for line in file.readlines():
            #print (line)
            resa = line.replace('}{',', ')
            print(resa)
            
        
        ret = json.loads(resa)
       # print(ret)
       # print(type(ret))
        
        
        resa1 = {'Date':None,'Time':None,'Doctor Name':None}
        #print(type(resa1))
        resultt =merge(resa1, ret)
        pprint(resultt, width=40)

        count = 0
        for c in resultt.values():
            if c is not None:
                count = count + 1
                print(count)
        if count == 3:
            dr = resultt["Doctor Name"]
            dt = resultt["Date"]
            di = resultt["Time"]
            
            
            full_response = {'Date':str(dt),'Time':str(di),'Doctor Name':str(dr),'text': 'Your appointment booking is successfull with {} for {} at {}'.format(dr,dt,di)}
            bod = ("Your appointment booking is successfull with {}  for {} at {}".format(dr,dt,di))
            message = client.messages \
            .create(
                 body= str(bod),
                 from_ ='+12058720907',
                 to ='+919109237197'
                    )   
            return json.dumps(full_response)
            os.remove("dict.txt")
             
        elif count == 2:
            if (resultt['Doctor Name'] != None and resultt['Date'] != None):
                Intent = "doctor_day"
                full_response = resultt
            elif(resultt['Date'] != None and resultt['Time'] != None):
                Intent = "day_time"
                full_response = resultt
            elif (resultt['Time'] != None and resultt['Doctor Name'] != None):
                Intent = "doctor_time"
                full_response = resultt
        elif count == 1: 
            if (resultt['Doctor Name'] != None):
                Intent = "doctor"
                full_response = resultt
            elif(resultt['Time'] != None):
                Intent = "time"
                full_response = resultt
            elif(resultt['Date'] != None):
                Intent = "day"
                full_response = resultt
                

        with open('./proj_reply.json') as json_data:
              intents = json.load(json_data)
        if intent:
              while intent:
                for i in intents['intents']:
                    print(i,Intent)
                    if i['tag'] == Intent:
                        if 'context_set' in i:
                            if show_details: print ('context:', i['contexit_set'])
                            context[userID] = i['context_set']

                        if not 'context_filter' in i or \
                            (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                            if show_details: print ('tag:', i['tag'])
                            full_response.update( {"text":str(random.choice(i['responses']))} )
                            return json.dumps(full_response)
              Intent.pop(0) 


app = Flask(__name__)
     

@app.route('/app', methods=["GET","POST"])
def my_form_post():
    text = request.get_json()
    res1 = json.dumps(text)
    text1 = response(res1)
    res2 = json.loads(text1)
    res3 = json.dumps(res2)
    #print(res3)
    return res3

@app.route('/', methods=["GET", "POST"])
def evaluate_get():
    text ={"text":"hello"}
    return json.dumps(text)

if __name__ == "__main__":
    print("* Starting web server... please wait until server has fully started")
    #app.run(host='103.24.173.234',port=4000)
    port = int(os.environ.get("PORT", 4000))
    app.run(host='0.0.0.0',port=port)
    #app.run()
