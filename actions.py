from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset, SlotSet
from order_DB import OrderDB
from bson.objectid import ObjectId

DB = OrderDB()

orderlist = []
ording = None
asking_field = None


class OrderMethod:
    ask = {
        "bool": lambda option: "請問要%s嗎" % option["name"],
        "group": lambda option: option["name"],
        "option": lambda option: "%s呢" % option["name"],
        "select": lambda option: "%s還是%s呢" % (" ".join(option["options"][:-1]), option["options"][-1])
    }

    @staticmethod
    def ask_option(dispatcher: CollectingDispatcher, tracker: Tracker) -> bool:
        if ording:
            for option in ording["options"]:
                if option["type"] == "group":
                    lost_all = True
                    lost_field = None
                    for field in option["options"].keys():
                        if field in ording["plus"].keys():
                            lost_all = False
                        elif not lost_all:
                            o = DB.get_option(option["options"][field])
                            dispatcher.utter_message(
                                OrderMethod.ask[o["type"]](o))
                            asking_field = field
                            return False
                        else:
                            lost_field = field
                    if lost_all:
                        dispatcher.utter_message(
                            OrderMethod.ask["option"](option))
                        return False
                    elif lost_field:
                        o = DB.get_option(option["options"][lost_field])
                        dispatcher.utter_message(
                            OrderMethod.ask[o["type"]](o))
                        asking_field = lost_field
                        return False
                elif not option["field"] in ording["plus"].keys():
                    dispatcher.utter_message(
                        OrderMethod.ask[option["type"]](option))
                    asking_field = option["field"]
                    return False
            return True
        else:
            dispatcher.utter_message(template="utter_noneOrder")
            return False

    @staticmethod
    def repeat_order(order):
        return "%d%s%s %s" % (order["count"], order["unit"], order["name"], order["plus"].values().join(" "))


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
            if ording:
                orderlist.append(ording)
                ording = None
            ording = {
                "_id": detail["_id"],
                "name": food,
                "count": int(count),
                "options": [DB.get_option(
                    option) for option in detail["options"]],
                "plus": {}
            }
            if OrderMethod.ask_option(dispatcher, tracker):
                orderlist.append(ording)
                ording = None
                dispatcher.utter_message("你點的是%d%s%s" %
                                         (int(count), detail["unit"], food))
                dispatcher.utter_message("請問還需要什麼嗎")
                return[AllSlotsReset()]
            else:
                return []
        else:
            dispatcher.utter_message("不好意思 我們沒有%s喔" % food)

        return []


class ActionStartOrder(Action):

    def name(self) -> Text:
        return "action_start_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global orderlist
        global ording
        orderlist = []
        ording = None

        dispatcher.utter_message(template="utter_startOrder")
        return [AllSlotsReset()]


class ActionOptionSelect(Action):
    def name(self) -> Text:
        return "action_option_select"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if intent == "ice_select" or intent == "ice_select+suger_select":
            ice = tracker.get_slot("ice_type")
            found = False

            for key in range(len(ording["options"])):
                if ording["options"][key]["_id"] == ObjectId("5edda69d338a12e97ab1a902"):
                    found = True
                    if ice in ording["options"][key]["options"]:
                        ording["plus"]["ice"] = ice
                    else:
                        dispatcher.utter_message(f"不好意思 我們沒有{ice}的選項喔")
                    break
                if ording["options"][key]["_id"] == ObjectId("5edda4ef338a12e97ab1a900"):
                    found = True
                    if ice in DB.get_option("5edda69d338a12e97ab1a902")["options"]:
                        ording["plus"]["ice"] = ice
                    else:
                        dispatcher.utter_message(f"不好意思 我們沒有{ice}的選項喔")
            if not found:
                dispatcher.utter_message("不好意思 %s沒有冰塊的選擇喔" % ording["name"])
        if intent == "suger_select" or intent == "ice_select+suger_select":
            suger = tracker.get_slot("suger_type")
            found = False
            for key in range(len(ording["options"])):
                if ording["options"][key]["_id"] == ObjectId("5edda69d338a12e97ab1a902"):
                    found = True
                    if suger in ording["options"][key]["options"]:
                        ording["plus"]["suger"] = suger
                    else:
                        dispatcher.utter_message(f"不好意思 我們沒有{suger}的選項喔")
                    break
                if ording["options"][key]["_id"] == ObjectId("5edda4ef338a12e97ab1a900"):
                    found = True
                    if suger in DB.get_option("5edda630338a12e97ab1a901")["options"]:
                        ording["plus"]["suger"] = suger
                    else:
                        dispatcher.utter_message(f"不好意思 我們沒有{suger}的選項喔")
            if not found:
                dispatcher.utter_message("不好意思 %s沒有甜度的選擇喔" % ording["name"])

        if OrderMethod.ask_option(dispatcher, tracker):
            dispatcher.utter_message(OrderMethod.repeat_order(ording))
            dispatcher.utter_message("請問還需要什麼嗎")


# class ActionStartOrder(Action):
# 	def name(self) -> Text:
# 		return "action_start_order"

# 	def run(self, dispatcher: CollectingDispatcher,
# 			tracker: Tracker,
# 			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
