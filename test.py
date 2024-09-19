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
title = []
for x in mycol.find():
    event_type = x.get("event_type", "N/A")
    dealerId=x.get("dealerId","N/A")
    if(event_type=='add_to_cart' and dealerId=="390"):
        product=x.get("products","N/A")[0].get("productId")    
        for y in mycol3.find():
            if y.get('_id')==ObjectId(product):
                title.append(y.get('title'))
finalTitle = list(set(title))
print(finalTitle)
# class test:
#     def testing(self):
#         dealername = ob.dealername(390)
#         remove_cart_product = obj.remove_cart_data_query_overall()
#         if remove_cart_product == None:
#             string = "No products were removed"
#         else:
#             string = f"Discarded product is {remove_cart_product}"
#         conversation_dict_1 = {"messages": [{"role": "system", "content": f"you are an assistant for dealer {dealername}"}, {"role": "user", "content": f"business name is {dealername}"}, {"role": "assistant", "content": "Nice name", "weight": 1}]}
#         conversation_dict_2 = {"messages": [{"role": "system", "content": f"you are an assistant for dealer {dealername}"}, {"role": "user", "content": "what is your name"}, {"role": "assistant", "content": "Name is InvenTreeFYBot", "weight": 1}]}
#         conversation_dict_3 = {"messages": [{"role": "system", "content": f"you are an assistant for dealer {dealername}"}, {"role": "user", "content": "most viewed catalog"}, {"role": "assistant", "content": f"most viewed catalogue is {obj.most_viewed_catalog()}", "weight": 1}]}
#         conversation_dict_4 = {"messages": [{"role": "system", "content": f"you are an assistant for dealer {dealername}"}, {"role": "user", "content": "most viewed catagory"}, {"role": "assistant", "content": f"most viewed catagory is {obj.most_viewed_catagory()}", "weight": 1}]}
#         conversation_dict_5 = {"messages": [{"role": "system", "content": f"you are an assistant for dealer {dealername}"}, {"role": "user", "content": "most viewed tag"}, {"role": "assistant", "content": f"most viewed tag is {obj.most_viewed_tag()}", "weight": 1}]}
#         conversation_dict_6 = {"messages": [{"role": "system", "content": f"you are an assistant for dealer {dealername}"}, {"role": "user", "content": "most viewed price range"}, {"role": "assistant", "content": f"most viewed price range is {obj.most_viewed_price_range()}", "weight": 1}]}
#         conversation_dict_7 = {"messages": [{"role": "system", "content": f"you are an assistant for dealer {dealername}"}, {"role": "user", "content": "most viewed product"}, {"role": "assistant", "content": f"most viewed product is {obj.most_viewed_product()}", "weight": 1}]}
#         conversation_dict_8 = {"messages": [{"role": "system", "content": f"you are an assistant for dealer {dealername}"}, {"role": "user", "content": "most discarded product"}, {"role": "assistant", "content": f"discarded product is {obj.remove_cart_data_query_overall()}", "weight": 1}]}
#         conversation_dict_9 = {"messages": [{"role": "system", "content": f"you are an assistant for dealer {dealername}"}, {"role": "user", "content": "products which user added to cart"}, {"role": "assistant", "content": f"{obj.add_to_cart()}", "weight": 1}]}
#         conversation_dict_10 = {"messages": [{"role": "system", "content": f"you are an assistant for dealer {dealername}"}, {"role": "user", "content": "product mostly removed from cart"}, {"role": "assistant", "content": f"{string}", "weight": 1}]}
#         conversation_dict_11 = {"messages": [{"role": "system", "content": f"you are an assistant for dealer {dealername}"}, {"role": "user", "content": "most interesting product"}, {"role": "assistant", "content": f"most interesting product is {obj.most_interesting_product()}", "weight": 1}]}
#         conversation_dict_12 = {"messages": [{"role": "system", "content": f"you are an assistant for dealer {dealername}"}, {"role": "user", "content": "most common search keyword"}, {"role": "assistant", "content": f"most common searched keyword is {obj.most_search_keyword()}", "weight": 1}]}
#         conversation_dict_13 = {"messages": [{"role": "system", "content": f"you are an assistant for dealer {dealername}"}, {"role": "user", "content": "most filtered category"}, {"role": "assistant", "content": f"most filtered category is {obj.most_filtered_category()}", "weight": 1}]}
#         conversation_dict_14 = {"messages": [{"role": "system", "content": f"you are an assistant for dealer {dealername}"}, {"role": "user", "content": "most filtered tag"}, {"role": "assistant", "content": f"most filtered tag is {obj.most_filtered_tag()}", "weight": 1}]}
#         conversation_dict_15 = {"messages": [{"role": "system", "content": f"you are an assistant for dealer {dealername}"}, {"role": "user", "content": "most applied price range"}, {"role": "assistant", "content": f"most applied price range is {obj.most_applied_price_range()}", "weight": 1}]}
#         conversation_dict_16 = {"messages": [{"role": "system", "content": f"you are an assistant for dealer {dealername}"}, {"role": "user", "content": "most applied price sorting"}, {"role": "assistant", "content": f"most applied sorting is {obj.most_applied_sorting()}", "weight": 1}]}
#         conversation_dict_17 = {"messages": [{"role": "system", "content": f"you are an assistant for dealer {dealername}"}, {"role": "user", "content": "highest selling product"}, {"role": "assistant", "content": f"highest selling product is {obj.highest_selling_product()}", "weight": 1}]}
#         conversation_dict_18 = {"messages": [{"role": "system", "content": f"you are an assistant for dealer {dealername}"}, {"role": "user", "content": "most inquiries came through"}, {"role": "assistant", "content": f"{obj.most_inquiry()}", "weight": 1}]}
#         conversation_dict_19 = {"messages": [{"role": "system", "content": f"you are an assistant for dealer {dealername}"}, {"role": "user", "content": "catalog with which user most interacted"}, {"role": "assistant", "content": f"{obj.catalog_impression()}", "weight": 1}]}
#         conversation_dict_20 = {"messages": [{"role": "system", "content": f"you are an assistant for dealer {dealername}"}, {"role": "user", "content": "from which location mostly user accessed"}, {"role": "assistant", "content": f"{obj.most_user_location()}", "weight": 1}]}
#         conversation_dict_21 = {"messages": [{"role": "system", "content": f"you are an assistant for dealer {dealername}"}, {"role": "user", "content": "every location from where user access"}, {"role": "assistant", "content": f"{obj.all_user_location()}", "weight": 1}]}
#         conversation_dict_22 = {"messages": [{"role": "system", "content": f"you are an assistant for dealer {dealername}"}, {"role": "user", "content": "from which device users access"}, {"role": "assistant", "content": f"{obj.user_device_type()}", "weight": 1}]}
#         conversation_dict_23 = {"messages": [{"role": "system", "content": f"you are an assistant for dealer {dealername}"}, {"role": "user", "content": "top 3 products"}, {"role": "assistant", "content": f"{obj.top_x_products("top 3 products")}", "weight": 1}]}
#         conversation_dict_24 = {"messages": [{"role": "system", "content": f"you are an assistant for dealer {dealername}"}, {"role": "user", "content": "top 4 products"}, {"role": "assistant", "content": f"{obj.top_x_products("top 4 products")}", "weight": 1}]}
#         conversation_dict_25 = {"messages": [{"role": "system", "content": f"you are an assistant for dealer {dealername}"}, {"role": "user", "content": "top 5 products"}, {"role": "assistant", "content": f"{obj.top_x_products("top 5 products")}", "weight": 1}]}
#         conversation_dict_26 = {"messages": [{"role": "system", "content": f"you are an assistant for dealer {dealername}"}, {"role": "user", "content": "most running store"}, {"role": "assistant", "content": f"{obj.most_running_store()}", "weight": 1}]}
#         # with open(f"training.jsonl", "a", encoding="utf-8") as initial:
#             # initial.truncate(0)
#             # json.dump(conversation_dict_1,initial)
#             # initial.write('\n')
#             # json.dump(conversation_dict_2,initial)
#             # initial.write('\n')
#             # json.dump(conversation_dict_3,initial)
#             # initial.write('\n')
#             # initial.truncate(0)
#             # for conversation in conversation_dicts:
#             #     json.dump(conversation, initial, cls=CustomEncoder)
#             #     initial.write('\n')
#         with open(f"training1.jsonl", "a", encoding="utf-8") as initial:
#             initial.truncate(0)
#             for name, value in locals().items():
#                 if name.startswith('conversation_dict_'):  # Filter to only fetch specific variables
#                     json.dump(value,initial)
#                     initial.write('\n')

# object1 = test()

# object1.testing()
