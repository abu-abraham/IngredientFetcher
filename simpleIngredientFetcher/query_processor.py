import vector_generator
from ingredientFetcher import models
from difflib import SequenceMatcher
import operator

import datetime
import vector_trainer

vocab_list = []
vector_map = dict()
full_list = []
word_1gram_dict = []

def get_dish(whole_message):
    global vocab_list,vector_map
    initialize_food_related_storage()
    return identify_dish(whole_message)

def initialize_food_related_storage():
    global vocab_list,vector_map
    if len(vocab_list) <= 0 or len(vector_map) <= 0:
        vector_map, vocab_list = vector_generator.return_vectors_of_all_dishes()

#Verified Ok
def identify_dish(whole_message):
    global vocab_list,vector_map
    query = ""
    for word in whole_message.split():
        if word in vocab_list:
            query+= (word+" ")
    return query

def ingredient_history_value(dish):
    #Hadle permuation
    try:
        sdish = models.Ingredients.objects.filter(dish=dish)
        return str(sdish[0].ingredients)
    except:
        print "not found"
        return None
    return None
    

def add_to_table(dish_name, result):
    p = models.Ingredients(dish=dish_name,ingredients=result);
    p.save();

def clearDB():
    models.Ingredients.objects.all().delete()

def is_dish(item):
    if item in vocab_list:
        return True
    return False

def log_user_query(fbid,dish,context):
    if len(dish)<=0:
        return;
    try:
        p = models.UserActivity.objects.get(userId=fbid)
        p.lastActive = datetime.datetime.now()
        p.topic = dish
        p.context = context
    except:
        p = models.UserActivity(userId=fbid,topic=dish,lastActive=datetime.datetime.now())
    p.save()

def earlier_query_relevant(fbid):
    try:
        p = models.UserActivity.objects.get(userId=fbid)
        print "user entry present"
        return True
    except:
        return False

def get_earlier_topic(fbid):
    p = models.UserActivity.objects.get(userId=fbid)
    print "returning old topic"
    return p.topic

def earlier_relavant_context(fbid):
    try:
        p = models.UserActivity.objects.get(userId=fbid)
        print p.context
        return p.context
    except:
        return 0

def check_and_correct_spellings(message):
    global full_list
    global word_1gram_dict
    message = str(message).lower()
    initialize_food_related_storage()
    if len(full_list)<=0:
        full_list = vector_trainer.get_full_list_of_words()
    if len(word_1gram_dict)<=0:
        word_1gram_dict = vector_trainer.generate_predictions_previous_word()
    message = message.split();
    w=""
    for index,word in enumerate(message):
        if word not in vocab_list:
            print vocab_list
            if word not in full_list:
                similar_list = get_most_similar_words(word)
                if index == 0:
                    most_probable_word = get_most_probable(similar_list,' ')
                else:
                    most_probable_word = get_most_probable(similar_list,message[index-1])
                if most_probable_word!="":
                    w+=(most_probable_word+" ")
                else:
                    w+=(word+" ")
            else:
                w+=(word+" ")
        else:
            w+=(word+" ")
    return w;

def get_most_similar_words(query_word):
    contender_list = []
    for word in full_list:
        if SequenceMatcher(None, query_word, word).ratio() > 0.75:
            contender_list.append(word)
    return contender_list

def get_most_probable(similar_list,previous_word):
    d = {}
    print len(word_1gram_dict)
    print len(full_list)
    for entry in similar_list:
        c = 0
        if not entry in word_1gram_dict:
            continue
        for p in word_1gram_dict[entry]:
            if p == previous_word:
                c=c+1
        prob = (c*100)/len(word_1gram_dict[entry])
        d[entry] = prob
    sorted_dictionary = sorted(d.items(), key=operator.itemgetter(1),reverse=True)
    if len(sorted_dictionary)>0:
        return sorted_dictionary[0][0]
    return ""
    





    
