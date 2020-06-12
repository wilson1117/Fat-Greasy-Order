from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset, SlotSet
from order_DB import OrderDB

DB = OrderDB()

orderlist = []
ording = None


class OrderMethod:
    ask = {
        "bool": lambda option: "請問要%s嗎" % option["name"],
        "group": lambda option: option["name"],
        "option": lambda option: "%s呢" % option["name"],
        "select": lambda option: "%s還是%s呢" % (option["options"][:-1].join(" "), option["options"][-1])
    }

    @staticmethod
    def ask_option(dispatcher: CollectingDispatcher, tracker: Tracker) -> bool:
        if ording:
            for option in ording["options"]:
                print(option)
                if option.__contains__("asked"):
                    continue
                dispatcher.utter_message(
                    OrderMethod.ask[option["type"]](option))
                return False
            return True
        else:
            dispatcher.utter_message(template="utter_noneOrder")
            return False


class ActionFoodOrder(Action):

    def name(self) -> Text:
        return "action_food_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food = tracker.get_slot("food")
        count = tracker.get_slot("count")

        if(not count.isdigit()):
            dispatcher.utter_message("不好意思 沒聽清楚")
            dispatcher.utter_message(template="utter_foodCount")
            return [SlotSet("count", None)]

        detail = DB.get_food_info(food)

        if(detail):
            global ording
            ording = {
                "_id": detail["_id"],
                "name": food,
                "count": int(count),
                "options": [DB.get_option(
                    option) for option in detail["options"]],
                "comment": []
            }
            if OrderMethod.ask_option(dispatcher, tracker):
                dispatcher.utter_message("你點的是%d%s%s" %
                                         (int(count), detail["unit"], food))
                dispatcher.utter_message("請問還需要什麼嗎")
            else:
                return[AllSlotsReset()]
        else:
            dispatcher.utter_message("不好意思 我們沒有%s喔" % food)

        return [AllSlotsReset()]


class ActionStartOrder(Action):

    def name(self) -> Text:
        return "action_start_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global orderlist
        orderlist = []
        dispatcher.utter_message(template="utter_startOrder")
        return []

# class ActionStartOrder(Action):
# 	def name(self) -> Text:
# 		return "action_start_order"

# 	def run(self, dispatcher: CollectingDispatcher,
# 			tracker: Tracker,
# 			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
