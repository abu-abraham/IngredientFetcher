import urllib2
import requests
import json
from lxml import html
from difflib import SequenceMatcher
import nltk
import query_processor

measurement_description_words = []

def extract(site):
    print site
    page = requests.get(site)
    tree = html.fromstring(page.content)
    items = tree.find_class("ingredient-description")
    items = tree.xpath('//div[@class="ingredient-description"]/text()')
    returnList = ""
    for line in items:
        if "None" not in line or line != "None":
            returnList += (line+", ")
    print returnList
    return returnList;


def find_ingredients(dish):
    keyBing = 'bing key'
    requestUrl = "https://api.cognitive.microsoft.com/bing/v7.0/search?q=taste.com "+dish+"&count=20&offset=0&mkt=en-us&safesearch=Moderate"
    r=requests.get(requestUrl, headers={"Ocp-Apim-Subscription-Key":"8d3a160774554744a07404917e54067b"})
    i = 0;
    word_map_prev = {}
    current_map = {}
    while i<10:
        print str(r.json()['webPages']['value'][i]['url'])
        if "taste.com" in str(r.json()['webPages']['value'][i]['url']) and not "collection" in str(r.json()['webPages']['value'][i]['url']):
            return trim_and_return(str(extract(str(r.json()['webPages']['value'][i]['url']))))
        i+=1;


def trim_and_return(result):
    #TODO: learn by extracting a lot and removing most common words in differnet context
    global measurement_description_words
    r_list = ""
    messurement_words= ['teaspoon','tablespoon','cup','spoon','spoons','tablespoons','teaspoons','cups','cut','into','dice','ml','l','more','add','serve','small','piece']
    decription_words = ['optional','ground','finely','roughly','crushed','toasted','grated','sliced','plain','chopped','thick','thin','fresh','see','note','cooked','trimmed']
    for item in result.split(","):
        item = ''.join([i for i in item if not i.isdigit()]) #Removing integers
        item = ' '.join([i for i in item.split() if presence_of_i_not_in(i,messurement_words)]) #Removing measurement words
        item = ' '.join([i for i in item.split() if presence_of_i_not_in(i,decription_words)]) #Removing decription words
        item = ' '.join([i for i in item.split() if len(i)>2]) #Removing words with less than 3 letters
        r_list+= (item + "\n")
    return r_list;

def presence_of_i_not_in(i,check_list):
    for entry in check_list:
        if SequenceMatcher(None, i, entry).ratio() > 0.7 and not query_processor.is_dish(i):
            return False
    return True



def find_recipie(dish):
    keyBing = 'bing key'
    requestUrl = "https://api.cognitive.microsoft.com/bing/v7.0/search?q=taste.com "+dish+"&count=10&offset=0&mkt=en-us&safesearch=Moderate"
    r=requests.get(requestUrl, headers={"Ocp-Apim-Subscription-Key":"8d3a160774554744a07404917e54067b"})
    i = 0;
    word_map_prev = {}
    current_map = {}
    while i<10:
        if "taste.com" in str(r.json()['webPages']['value'][i]['url']):
            return str(r.json()['webPages']['value'][i]['url']);
        i+=1;
