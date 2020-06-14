from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset, SlotSet
from order_DB import OrderDB
from bson.objectid import ObjectId

DB = OrderDB()

orderlist = []
ordering = None
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
        if ordering:
            for option in ordering["options"]:
                if option["type"] == "group":
                    lost_all = True
                    lost_field = None
                    for field in option["options"].keys():
                        if field in ordering["plus"].keys():
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
                elif not option["field"] in ordering["plus"].keys():
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
        return "%d%s%s %s" % (
            int(order["count"]),
            order["unit"],
            order["name"],
            " ".join(order["plus"].values())
        )


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
            global ordering
            if ordering:
                orderlist.append(ordering)
                ordering = None
            ordering = {
                "_id": detail["_id"],
                "unit": detail["unit"],
                "name": food,
                "price": detail["price"],
                "count": int(count),
                "options": [DB.get_option(
                    option) for option in detail["options"]],
                "plus": {}
            }
            if OrderMethod.ask_option(dispatcher, tracker):
                orderlist.append(ordering)
                ordering = None
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
        global ordering
        orderlist = []
        ordering = None

        dispatcher.utter_message(template="utter_startOrder")
        return [AllSlotsReset()]


class ActionOptionSelect(Action):
    def name(self) -> Text:
        return "action_option_select"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if intent == "suger_select" or intent == "ice_select+suger_select":
            suger = tracker.get_slot("suger_type")
            found = False
            for key in range(len(ordering["options"])):
                if ordering["options"][key]["_id"] == ObjectId("5edda69d338a12e97ab1a902"):
                    found = True
                    if suger in ordering["options"][key]["options"]:
                        ordering["plus"]["suger"] = suger
                    else:
                        dispatcher.utter_message(f"不好意思 我們沒有{suger}的選項喔")
                    break
                if ordering["options"][key]["_id"] == ObjectId("5edda4ef338a12e97ab1a900"):
                    found = True
                    if suger in DB.get_option("5edda630338a12e97ab1a901")["options"]:
                        ordering["plus"]["suger"] = suger
                    else:
                        dispatcher.utter_message(f"不好意思 我們沒有{suger}的選項喔")
            if not found:
                dispatcher.utter_message("不好意思 %s沒有甜度的選擇喔" % ordering["name"])
        if intent == "ice_select" or intent == "ice_select+suger_select":
            ice = tracker.get_slot("ice_type")
            found = False

            for key in range(len(ordering["options"])):
                if ordering["options"][key]["_id"] == ObjectId("5edda69d338a12e97ab1a902"):
                    found = True
                    if ice in ordering["options"][key]["options"]:
                        ordering["plus"]["ice"] = ice
                    else:
                        dispatcher.utter_message(f"不好意思 我們沒有{ice}的選項喔")
                    break
                if ordering["options"][key]["_id"] == ObjectId("5edda4ef338a12e97ab1a900"):
                    found = True
                    if ice in DB.get_option("5edda69d338a12e97ab1a902")["options"]:
                        ordering["plus"]["ice"] = ice
                    else:
                        dispatcher.utter_message(f"不好意思 我們沒有{ice}的選項喔")
            if not found:
                dispatcher.utter_message("不好意思 %s沒有冰塊的選擇喔" % ordering["name"])
        if intent == "size_select":
            size = tracker.get_slot("size")
            found = False
            for key in range(len(ordering["options"])):
                if ordering["options"][key]["_id"] == ObjectId("5ede2ded338a12e97ab1a903"):
                    found = True
                    if size in ordering["options"][key]["options"]:
                        ordering["plus"]["size"] = size
                    else:
                        dispatcher.utter_message(f"不好意思 我們沒有{size}的選項喔")
                    break
            if not found:
                dispatcher.utter_message("不好意思 %s沒有大小的選擇喔" % ordering["name"])
        if OrderMethod.ask_option(dispatcher, tracker):
            dispatcher.utter_message(OrderMethod.repeat_order(ordering))
            dispatcher.utter_message("請問還需要什麼嗎")


class ActionOrderCheck(Action):
    def name(self) -> Text:
        return "action_order_check"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global ordering
        global orderlist
        if ordering:
            orderlist.append(ordering)
            ordering = None
        sum = 0
        dispatcher.utter_message("您點的是")
        for order in orderlist:
            price = int(order["count"] * (order["price"] + [0, 15][(
                "size" in order["plus"].keys()) and order["plus"]["size"] == "大杯"]))
            dispatcher.utter_message(
                "%s %d元" % (OrderMethod.repeat_order(order), price))
            sum += price
        dispatcher.utter_message("一共是%d元" % sum)
        dispatcher.utter_message("餐點是否無誤")
        return []


class ActionSendOrder(Action):
    def name(self) -> Text:
        return "action_send_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global ordering
        global orderlist
        global asking_field
        food = [{
            "name": order["name"],
            "plus": order["plus"],
            "count": order["count"]
        } for order in orderlist]
        DB.insert_order({"food": food})
        dispatcher.utter_message("訂單已送出")
        dispatcher.utter_message("謝謝惠顧")
        orderlist = []
        ordering = None
        asking_field = None
        return [AllSlotsReset()]
