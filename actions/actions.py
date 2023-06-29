# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import csv


ALLOWED_SOURCE = ["salesforce", "hubspot", "slack", "sheets"]
ALLOWED_DESTINATION = ["salesforce", "hubspot", "slack", "sheets"]
ALLOWED_SOURCE_VARIABLE = ["Update Field on Record", "New Contact", "New Task", "New Lead", "New Account", "New Opportunity"]
ALLOWED_DESTINATION_VARIABLE = ["Create Speadsheet", "Delete Row", "Update Row", "Create Spreadsheet row", "Update Speadsheet row"]

class ValidateConnectorForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_connector_form"

    
    def validate_source(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate source value."""

        with open('Connectors.csv', 'r') as file:
            reader = csv.DictReader(file)
            output = [row for row in reader if row['Trigger API'] == slot_value.lower()]
            #print(output)
        if output: 
            # reply  = f"This is a list of universities in {location}:"
            # reply += "\n- " + "\n- ".join([item['College'] for item in output])
            dispatcher.utter_message(text=f"OK! You want to have a connection from {slot_value}")
            return {"source": slot_value}
        else: 
            dispatcher.utter_message(text=f"We dont have connector from {slot_value} you can try Salesforce, Hubspot, Slack, Sheets etc")
            return {"source": None}

    def validate_destination(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate destination value."""

        with open('Connectors.csv', 'r') as file:
            reader = csv.DictReader(file)
            source = tracker.get_slot("source").lower()
            output = [row for row in reader if (row['Trigger API']==source and row['Action API'] == slot_value.lower())]
            print(source)
            #print(output)
        if output: 
            # reply  = f"This is a list of universities in {location}:"
            # reply += "\n- " + "\n- ".join([item['College'] for item in output])
            dispatcher.utter_message(text=f"OK! You want to have a connection from {slot_value}")
            return {"destination": slot_value}
        else: 
            dispatcher.utter_message(text=f"We dont have connector to {slot_value} you can try Salesforce, Hubspot, Slack, Sheets etc")
            return {"destination": None}

        # if slot_value not in ALLOWED_DESTINATION:
        #     dispatcher.utter_message(text=f"We only have connectors for Salesforce, Hubspot, Slack and Sheets")
        #     return {"destination": None}
        # dispatcher.utter_message(text=f"OK! You want to have a connection to {slot_value}")
        # return {"destination": slot_value}
      
    def validate_source_variable(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate source_variable value."""

        with open('Connectors.csv', 'r') as file:
            reader = csv.DictReader(file)
            source = tracker.get_slot("source").lower()
            destination = tracker.get_slot("destination").lower()
            output = [row for row in reader if (row['Trigger API']==source and row['Action API'] == destination)]
            print((output[0]['Trigger Variables']))
            variables = False
            if(slot_value in output[0]['Trigger Variables']):
                variables = True
            print(variables)
        if variables: 
            # reply  = f"This is a list of universities in {location}:"
            # reply += "\n- " + "\n- ".join([item['College'] for item in output])
            dispatcher.utter_message(text=f"OK! The connection will have {slot_value} variable from {source}")
            return {"source_variable": slot_value}
        else: 
            dispatcher.utter_message(text=f"We dont have this variable right now")
            return {"source_variable": None}

        # if slot_value.lower() not in ALLOWED_SOURCE_VARIABLE:
        #     dispatcher.utter_message(text=f"We only have these variables: {'/'.join(ALLOWED_SOURCE_VARIABLE)}")
        #     return {"source_variable": None}
        # dispatcher.utter_message(text=f"OK! You want to have {slot_value} as source variable.")
        # return {"source_variable": slot_value}

    def validate_destination_variable(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate destination_variable value."""

        with open('Connectors.csv', 'r') as file:
            reader = csv.DictReader(file)
            source = tracker.get_slot("source").lower()
            destination = tracker.get_slot("destination").lower()
            output = [row for row in reader if (row['Trigger API']==source and row['Action API'] == destination)]
            print((output[0]['Action Variables']))
            variables = False
            if(slot_value in output[0]['Action Variables']):
                variables = True
            print(variables)
        if variables: 
            # reply  = f"This is a list of universities in {location}:"
            # reply += "\n- " + "\n- ".join([item['College'] for item in output])
            dispatcher.utter_message(text=f"OK! The connection will have {slot_value} variable to {destination}")
            return {"destination_variable": slot_value}
        else: 
            dispatcher.utter_message(text=f"We dont have this variable right now")
            return {"destination_variable": None}
    
        # if slot_value not in ALLOWED_DESTINATION_VARIABLE:
        #     dispatcher.utter_message(text=f"I don't recognize that variable. We only have these variables {'/'.join(ALLOWED_DESTINATION_VARIABLE)}.")
        #     return {"destination_variable": None}
        # dispatcher.utter_message(text=f"OK! You want to have {slot_value} as the variable to be connected to ")
        # return {"destination_variable": slot_value}
