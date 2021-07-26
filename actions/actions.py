# This file contains custom actions for the chatbot ABIE.
# It runs custom Python code in conjunction with Rasa Open Source.
#
# Feminist Chatbot ABIE, Version 2.1
# Created by David Romero, MSc Student- University of Warwick
# July 2021.

from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import datetime as dt
import csv

# Data files with Gender Pay Gap statistics: countries and UK companies
GPG_INTL_PATH = "actions/gpg_intl.csv"
GPG_UK_PATH = "actions/gpg_uk.csv"

class ActionGetTime(Action):
# This class obtains the current time and sends back a message to the user,
# displaying hh:mm am/pm formatting.   
    
     def name(self) -> Text:
         return "action_show_time"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         current_time =  dt.datetime.now()
         reply = "Where I am it's " + current_time.strftime("%I:%M %p").lstrip("0")
         dispatcher.utter_message(text = reply)

         return []

class ActionGetGPGIntl(Action):
# Class that queries a separate text file with gender pay gap statistics for
# various countries: Western Europe, North America, a couple in South America
# and some in Asia Pacific incl. AU, NZ, SG, KR and JP.
    
     def name(self) -> Text:
         return "action_get_gpg_intl"
     
     def __init__(self) -> None:
        self.gpg_file = GPG_INTL_PATH

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                  
         ctry_name = tracker.get_slot('country')
         gpg_dict = {}         
         with open(self.gpg_file) as f:
             reader = csv.reader(f)
             for row in reader:
                 key = row[0]
                 gpg_val = row[1]
                 gpg_dict[key] = gpg_val
                 
         report_yr = '2019' # Latest statistics available in July 2021.
         try:
             ctry_name_folded = ctry_name.casefold()
             gpg_result = gpg_dict[ctry_name_folded]
         except KeyError:
             reply = "{}{}".format("I'm sorry, I don't have gender pay gap information for ", ctry_name)
         else:
             reply = "{}{}{}{}{}{}{}".format("The avg. gender pay gap in ", report_yr, " in ", ctry_name.title(), " was ", gpg_result, "%")
         
         dispatcher.utter_message(text = reply)         
         # Need to reset all slots in case user wants to see a different ctry.
         return [AllSlotsReset()] 

class ActionGetGPGUK(Action):
# Class that queries separate text file with gender pay gap statistics for
# several UK-based companies that are legally required to report gpg.
# Latest complete report from uk.gov.uk includes 2020.

     def name(self) -> Text:
         return "action_get_gpg_uk"
     
     def __init__(self) -> None:
        self.gpg_file = GPG_UK_PATH
        

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         company = tracker.get_slot('company')
         gpg_dict = {}
         with open(self.gpg_file) as f:
             reader = csv.reader(f)
             for row in reader:
                 key = row[0]
                 gpg_val = row[1]
                 gpg_dict[key] = gpg_val
                 
         report_yr = '2020' # Latest statistics available in July 2021.
         try:
             company_folded = company.casefold()
             gpg_result = gpg_dict[company_folded]
         except KeyError:
             reply = "{}{}".format("I'm sorry, I don't have gender pay gap information for ", company)
         else:
             reply = "{}{}{}{}{}{}{}".format("The avg. gender pay gap in ", report_yr, " at ", company, " was ", gpg_result, "%")

         dispatcher.utter_message(text = reply)
         # Need to reset all slots in case user wants to see a different company.
         return [AllSlotsReset()]


""" THIS SECTION CAN BE USED TO ASK AND STORE THE USER'S NAME.
    THIS PART LEFT OUT OF SCOPE FOR FINAL VERSION OF CHATBOT,
    DUE TO PRIVACY CONCERNS WHEN ASKING USERS TO TEST THE BOT.

class ActionReceiveName(Action):
# This class supports a custom action to receive the name of the user.
# It populates the slot 'name' and keeps track of it during the conversation.
    
    def name(self) -> Text:
        return "action_receive_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        text = tracker.latest_message['text']
        dispatcher.utter_message(text=f"I'll remember your name {text}!")
        return [SlotSet("name", text)]


class ActionSayName(Action):
# This class supports a custom action to say or repeat the name of the user.
# If the slot 'name' is empty the bot doesn't know and replies accordingly.

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
"""