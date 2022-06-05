# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
import random
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
import json


def haystack_run(message):
    headers = {
        'Content-Type': 'application/json',
    }

    params = (
        ('pretty', ''),
    )

    data = '{"query": \"' + message + '\" , "params": {"NYUProfRetriever": {"top_k": 1}}}'
    print(data)
    response = requests.post('http://10.214.14.48/queryprof', headers=headers, params=params, data=data)
    print(response.json())
    return response.json()['answers'][0]['answer']


class ActionHaystack(Action):

    def name(self) -> Text:
        return "call_haystack"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = tracker.latest_message.get('text')
        dispatcher.utter_message(text=haystack_run(message))
        return []


class ClassroomHaystack(Action):
    def name(self) -> Text:
        return "get_class_info"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        q = "Where is {}'s office".format(tracker.get_slot('name'))
        haystack_response = haystack_run(q)
        dispatcher.utter_message(text=haystack_response)
        return []
