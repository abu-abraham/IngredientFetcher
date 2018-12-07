from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.http import JsonResponse
import json,requests
import sys
import bingExtraction
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import query_processor
import query_parser

def post_facebook_message(fbid, recevied_message):   
    access = "EAAbfKFmzqN8BAMzCIjDOFjV8rZBnUbn0bEt7qqYCWfa9gW4q1lI1RUu3PKsRpG6dOf1RJav85Dr1vtLYNjfYriPuIBU8cpOM7zMa3ryot7pMjybKsTvFUHqKMecrp2PS4hDROv39ZAURZCLkZCoySNQ0Lb2whqwOk4i54l5gjwZDZD";        
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+access 
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":return_ingredients(recevied_message,fbid)}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    print(status.json())

def return_ingredients(whole_message,fbid):
    whole_message=query_processor.check_and_correct_spellings(whole_message);
    print whole_message
    whole_message = query_parser.format_message(whole_message);
    if query_parser.message_type(whole_message) == query_parser.MessageType.Greeting:
        return "Hey there :)"
    #Find dish from message
    operation = query_parser.parse_operation(whole_message, fbid)
    print operation
    if operation == query_parser.Operation.Ingredient:
        dish = query_processor.get_dish(whole_message)
        if len(dish)<=0:
            print "trying to link with earlier question"
            if query_processor.earlier_query_relevant(fbid):
                dish = query_processor.get_earlier_topic(fbid)
                whole_message+= " "+dish
                print "earlier topic was "+dish
            else:
                return "Sorry, couldn't understand the query. I am just a few days old, hopefully I will be a good learner :)"
        query_processor.log_user_query(fbid,dish,query_parser.Operation.Ingredient)
        value_in_DB = query_processor.ingredient_history_value(dish);
        if value_in_DB != None:
            print "Stored result"
            return value_in_DB;
        result = bingExtraction.find_ingredients(dish)
        if result == None or len(result) <= 0: 
            with open('not_found.csv','a') as f:
                f.write(whole_message)
                f.write('\n')
            return "Sorry, not found"
        query_processor.add_to_table(dish, result)
        return result;

    elif operation == query_parser.Operation.Recipie:
        dish = query_processor.get_dish(whole_message)
        if len(dish)<=0:
            print "trying to link with earlier question"
            if query_processor.earlier_query_relevant(fbid):
                dish = " "+query_processor.get_earlier_topic(fbid)
            else:
                return "Sorry, couldn't understand the query. I am just a few days old, hopefully I will be a good learner :)"
        query_processor.log_user_query(fbid,dish,query_parser.Operation.Recipie)
        url = bingExtraction.find_recipie(dish)
        return "I am just an Ingredient Fetcher, but I have heard rave reviews about taste.com, check out their recipie : "+url
    else:
        return "Sorry, couldn't understand the query. I am just a few days old, hopefully I will be a good learner :)"



def get_ingredients(self,dish):
    result = bingExtraction.find_ingredients(dish)
    if len(result) <= 0: 
        result = "Sorry, not found"
    response = JsonResponse(result,safe=False)
    return response;

class FacebookView(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.GET.get('hub.verify_token') == '123':
            return HttpResponse(request.GET.get('hub.challenge'))
        else:
            return HttpResponse('Error, invalid token')

    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    print "recieved message "
                    print(message)  
                    post_facebook_message(message['sender']['id'], message['message']['text'])   
        return HttpResponse()
