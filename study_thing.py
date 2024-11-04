from datetime import datetime
import os
from flask import Flask
from googlesearch import search
import html2text
import requests
os.environ['OPENAI_API_KEY'] = '*****************************************************************************************************'#replace with your own
from openai import OpenAI
h = html2text.HTML2Text()
h.ignore_links = True
app = Flask(__name__)
#thing = "&quot ask/ &quot  + "
thing = "&quot link_selector/ &quot  + "
thing2 = "&quot ask/ &quot  + "

import googlesearch
@app.route("/")
def home():
    return "<input type='text' val='' id='question'> <a href='javascript:void(0);' onclick='this.href = "+thing+"document.getElementById(&quot;question&quot;).value;'>find link</a>"
#return "<input type='text' val='' id='question'> <a href='javascript:void(0);' onclick='this.href = "+thing+"document.getElementById(&quot;question&quot;).value;'>ask</a>"

@app.route("/link_selector/<thing>")
def link_thing(thing):
  idx = 0
  html_text = '' 
  for i in search(thing, num_results=20, lang='en'):
    idx+=1
    html_text+=f"<br> {idx}. <a href='javascript:void(0);' onclick='this.href = "+thing2+f" &quot {i.replace('/','|')} &quot '>{i}</a>"
  return html_text


@app.route("/link_selector/ask/<thing>")
def asker(thing):
    
    client = OpenAI()
    a_link = '/link_selector/ask/\%20\%20'
    completion = client.chat.completions.create(
    model="gpt-4o-mini-2024-07-18",
    messages=[
      {"role": "system", "content": "You are a person who uses has good summarizing skills"},
      {"role": "user", "content": f"Convert this to notes(provide details and make it like for a test): {h.handle(requests.get(thing.replace('|','/').replace(a_link,'')).text)} seperate it into sections with a tag ____ and don't bold ANY text"}
    ]
  )
    ans = completion.choices[0].message.content.split('____')
    stuff = ''
    for i in range(0,len(ans)):
      stuff += ("<p>"+ans[i]+"</p>"+'<br>')
    thing3 = f"/questions/{thing}"
    return "<div>"+stuff+f"<a href='{thing3}'><button>click to get quized on</button></a></div>"
@app.route('/questions/<thing>')
def questioner(thing):
  return f"""
    <p>Difficulty (1-3)</p>
    <input type='text' value='' id='difficulty'>
    <p>Number of questions</p>
    <input type='text' value='' id='num'>
    <a href='javascript:void(0);' 
       onclick='this.href = "/test/" + 
                document.getElementById("num").value + "/" + 
                document.getElementById("difficulty").value + "/" + 
                "{thing.replace('/', '|')}"'>
        Generate Questions
    </a>
    """
@app.route('/test/<thing>/<thing2>/<thing3>')
def tester(thing,thing2,thing3):
  client = OpenAI()
  real_difficulty = ['easy','medium','hard'][int(thing2)-1]
  completion = client.chat.completions.create(
    model="gpt-4o-mini-2024-07-18",
    messages=[
      {"role": "system", "content": "You are a person who uses has good summarizing skills"},
      {"role": "user", "content": f"Make a quiz with {real_difficulty}{thing} questions using this text: {h.handle(requests.get(thing3.replace('|','/')).text)} split the questions into a thing like QUESTION:(blah blah blah) ANSWER:(blah blah blah) and don't bold the text and don't say anything else"}
    ]
  )
  return '<p>'+completion.choices[0].message.content+'</p>'
