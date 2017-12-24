from difflib import SequenceMatcher
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer
import inflect
import query_processor

class Operation:
    Recipie = 1
    Ingredient = 2
    NotFound = 3
    RecipieRepeat = 4

class MessageType:
    Conversation = 1
    Greeting = 2
    Query = 3

def parse_operation(message,fbid):
    dish = query_processor.get_dish(message)
    message = message.split()
    dish = dish.split()
    print "here - 1"
    if any_related_in(["recipie","step","how","guide"],message):
        return Operation.Recipie
    pos = get_position(dish,message)
    if pos > 0 and (any_related_in(["make","ingredient"],message[pos-1]) or (pos-1 > 0 and related_in("for",message[pos-1]))):
        return Operation.Ingredient
    elif len(message) == len(dish):
        return Operation.Ingredient
    elif related_in("ingredient",message):
        return Operation.Ingredient
    elif query_processor.earlier_relavant_context(fbid) > 0:
        return query_processor.earlier_relavant_context(fbid)
    else:
        return Operation.NotFound

def any_related_in(wordlist,message):
    for word in wordlist:
        if related_in(word,message):
            return True
    return False

def related_in(word, message):
    if word in message:
        return True
    else:
        syns = wordnet.synsets(word)
        for item in syns:
            if item.lemmas()[0].name() in message:
                print item.lemmas()[0].name()
                return True
    return False

def get_position(dish,message):
    j = 0
    i = 0
    for index,word in enumerate(message):
        if j< len(dish) and word == dish[j]:
            if j == 0:
                i = index
            j+=1
    if j == len(dish):
        return i
    

def format_message(whole_message):
    whole_message = str(whole_message).lower()
    formatted_msg = ""
    p = inflect.engine()
    for word in whole_message.split():
        if str(p.singular_noun(word))!="False":
            formatted_msg+=(p.singular_noun(word)+" ")
        else:
            formatted_msg+=(word+" ")
    return formatted_msg.strip()          

def message_type(whole_message):
    whole_message = whole_message.lower()
    if any_related_in(["hello","hey"],whole_message):
        return MessageType.Greeting
    else:
        return MessageType.Query

