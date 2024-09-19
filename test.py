from pymongo import MongoClient
from bson.json_util import dumps
from bson import ObjectId
from sql import *
from fetchdata import *
import json
from datetime import datetime
ob = Main()
client=MongoClient("mongodb://localhost:27017/")
mydb2 = client["ilsdb"] 
mycol = mydb2["catalog_data"]
mycol3 = mydb2["inventory"]

obj = DataFetch(390)
# class CustomEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, set):
#             return list(obj)
#         return super().default(obj)
# title = []
# for x in mycol.find():
#     event_type = x.get("event_type", "N/A")
#     dealerId=x.get("dealerId","N/A")
#     if(event_type=='add_to_cart' and dealerId=="390"):
#         product=x.get("products","N/A")[0].get("productId")    
#         for y in mycol3.find():
#             if y.get('_id')==ObjectId(product):
#                 title.append(y.get('title'))
# finalTitle = list(set(title))
# print(finalTitle)

import spacy

# Load a pre-trained English model
nlp = spacy.load("en_core_web_sm")

# Example text
text = "catalog 1.0 Catalog V1"

# Process the text
doc = nlp(text)

# Extract entities
for ent in doc.ents:
    print(ent.text, ent.label_)