from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset


class ActionFoodOrder(Action):

    def name(self) -> Text:
        return "action_foodOrder"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food = tracker.get_slot("food")
        count = tracker.get_slot("count")

        if count.isdigit():
            dispatcher.utter_message("你點的是 %d 個 %s" % (int(count),food))
        else:
            dispatcher.utter_message("你點的是 1 份 %s" % food)
        return [AllSlotsReset()]
