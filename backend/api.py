from flask import Flask, Response, request
from flask_api import status
import pymongo
from bson import ObjectId
import json

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["order"]
orderList =  db.orderList

@app.route("/")
def hello():
    print(list(orderList.find()))
    getOrder = list(orderList.find())
    for index in range(len(getOrder)):
        getOrder[index]["_id"] = str(getOrder[index]["_id"])
    return Response(headers={'Access-Control-Allow-Origin': '*'}, status=status.HTTP_200_OK, response=json.dumps(getOrder))

@app.route("/del_order")
def delete():
    print(request.args)
    orderList.remove({"_id": ObjectId(request.args.get("_id"))})
    return Response(headers={'Access-Control-Allow-Origin': '*'},status=status.HTTP_200_OK,response='qqq')



if __name__ == "__main__":
    app.run(port=8000)