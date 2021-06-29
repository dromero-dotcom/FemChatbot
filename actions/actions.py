# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

#import pandas as pd
import datetime as dt
import csv

GPG_INTL_PATH = "actions/gpg_intl.csv"
GPG_UK_PATH = "actions/gpg_uk.csv"

class ActionHelloWorld(Action):

     def name(self) -> Text:
         return "action_hello_world"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message(text="I'm very glad to hear that!")

         return []

class ActionGetTime(Action):

     def name(self) -> Text:
         return "action_show_time"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         current_time =  dt.datetime.now()
         reply = "It's " + current_time.strftime("%I:%M %p")
         dispatcher.utter_message(text = reply)

         return []

class ActionGetGPGIntl(Action):

     def name(self) -> Text:
         return "action_get_gpg_intl"
     
     def __init__(self) -> None:
        self.gpg_file = GPG_INTL_PATH

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                  
         ctry_name = tracker.get_slot('country')
         #ctry_name = tracker.latest_message['text']
         gpg_dict = {}
         """
         gpg_dict['Austria']= '20'
         gpg_dict['Germany']= '19'
         gpg_dict['Mexico']= '18.8'
         gpg_dict['USA']= '18.5'
         """
         
         with open(self.gpg_file) as f:
             reader = csv.reader(f)
             #header_row = next(reader)
             for row in reader:
                 key = row[0]
                 gpg_val = row[1]
                 gpg_dict[key] = gpg_val
                 
         #ctry_name = 'Germany'
         report_yr = '2019'
         try:
             gpg_result = gpg_dict[ctry_name]
         except KeyError:
             reply = "{}{}".format("I'm sorry, I don't have gender pay gap information for ", ctry_name)
         else:
             reply = "{}{}{}{}{}{}{}".format("The avg. gender pay gap in ", report_yr, " in ", ctry_name, " was ", gpg_result, "%")
         
         dispatcher.utter_message(text = reply)

         #return [SlotSet("country", ctry_name2)]
         return [AllSlotsReset()]

class ActionGetGPGUK(Action):

     def name(self) -> Text:
         return "action_get_gpg_uk"
     
     def __init__(self) -> None:
        self.gpg_file = GPG_UK_PATH
        

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         company = tracker.get_slot('company')
         #company = tracker.latest_message['text']
         gpg_dict = {}
         """
         gpg_dict['Google UK']= '17'
         gpg_dict['HSBC']= '33'
         gpg_dict['Tesco']= '9.7'
         """
         #gpg_file = 'gpg_uk.csv'
         with open(self.gpg_file) as f:
             reader = csv.reader(f)
             #header_row = next(reader)
             for row in reader:
                 key = row[0]
                 gpg_val = row[1]
                 gpg_dict[key] = gpg_val
                 
         #company = 'Google UK'
         report_yr = '2020'
         try:
             gpg_result = gpg_dict[company]
         except KeyError:
             reply = "{}{}".format("I'm sorry, I don't have gender pay gap information for ", company)
         else:
             reply = "{}{}{}{}{}{}{}".format("The avg. gender pay gap in ", report_yr, " at ", company, " was ", gpg_result, "%")

         dispatcher.utter_message(text = reply)

         #return [SlotSet("company", company2)]
         return [AllSlotsReset()]
     
class ActionReceiveName(Action):

    def name(self) -> Text:
        return "action_receive_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        text = tracker.latest_message['text']
        dispatcher.utter_message(text=f"I'll remember your name {text}!")
        return [SlotSet("name", text)]


class ActionSayName(Action):

    def name(self) -> Text:
        return "action_say_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name")
        if not name:
            dispatcher.utter_message(text="I don't know your name.")
        else:
            dispatcher.utter_message(text=f"Your name is {name}!")
        return []        
