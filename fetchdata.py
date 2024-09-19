from sql import *
from bson import ObjectId
from collections import Counter
from pymongo import MongoClient
from heapq import nlargest
from collections import Counter
import re
from word2number import w2n

client=MongoClient("mongodb://localhost:27017/")
mydb2 = client["ilsdb"] 
mycol = mydb2["catalog_data"]
mycol3 = mydb2["inventory"]

ob = Main()


class DataFetch():
    def __init__(self, dealerid):
        self.dealerid = dealerid

    def remove_cart_data_query_overall(self):
        data = []
        for x in mycol.find():
            event_type = x.get("event_type", "N/A")
            dealerId=x.get("dealerId","N/A")
            if(event_type=='remove_cart_data' and dealerId==self.dealerid):
                product=x.get("products","N/A")[0].get("productId")    
                for y in mycol3.find():
                    if y.get('_id')==ObjectId(product):
                        title = y.get('title')
                        data.append(title)
        data1 = list(set(data))
        return data1
    
    def most_removed_product(self):
        title=[] 
        for x in mycol.find():
            event_type = x.get("event_type", "N/A")
            dealerId=x.get("dealerId","N/A")
            if(event_type=='remove_cart_data' and dealerId==self.dealerid):
                product=x.get("products","N/A")[0].get("productId")    
                for y in mycol3.find():
                    if y.get('_id')==ObjectId(product):
                        title.append(y.get('title'))
        occurrence = {item: title.count(item) for item in title}  
        Key_max = max(zip(occurrence.values(), occurrence.keys()))[1]  
        return Key_max
    
    # def remove_cart_data_query_catalog(self):
    #     mycursor = mydb1.cursor() 
    #     mycursor.execute(f"select uuid from tblinvseclinks where secure_link_title='{catalog}' and dealer_id={dealer}") 
    #     myresult = mycursor.fetchone()
    #     if(myresult==None):
    #         print("There is no catalog with such name.")
    #     else:
    #         catalogfetchid=str(myresult[0])
    #         title=[] 
    #         gettitle=[]
    #         count_remove_product=mycol.count_documents({ 
    #                     "event_type": "remove_cart_data",
    #                     "dealerId": self.dealerid,
    #                     "catalogId":catalogfetchid
    #                 })
    #         if(count_remove_product>0):
    #             for x in mycol.find():
    #                 event_type = x.get("event_type", "N/A")
    #                 dealerId=x.get("dealerId","N/A")
    #                 catalogId=x.get("catalogId","N/A")
    #                 if(event_type=='remove_cart_data' and dealerId==self.dealerid and catalogId==catalogfetchid):
    #                     product=x.get("products","N/A")[0].get("productId")    
    #                     for y in mycol3.find():
    #                         if y.get('_id')==ObjectId(product):
    #                             title.append(y.get('_id'))
    #             occurrence = {item: title.count(item) for item in title} 
    #             if(all(x==list (occurrence.values())[0] for x in occurrence.values())==True):
    #                 for x in mycol.find():
    #                     event_type = x.get("event_type", "N/A")
    #                     dealerId=x.get("dealerId","N/A")
    #                     catalogId=x.get("catalogId","N/A")
    #                     if(event_type=='remove_cart_data' and dealerId==self.dealerid and catalogId==catalogfetchid):
    #                         product=x.get("products","N/A")[0].get("productId")    
    #                         for y in mycol3.find():
    #                             if y.get('_id')==ObjectId(product):
    #                                 gettitle.append(y.get('title'))
    #                 print(gettitle)
    #             else:
    #                 Key_max = max(zip(occurrence.values(), occurrence.keys()))[1]
    #                 for y in mycol3.find():
    #                     if y.get('_id')==ObjectId(Key_max):
    #                         print(y.get('title'))
    #         else:
    #             return f"No product discarded for {catalog}"
    
    def most_viewed_catalog(self):
        result = mycol.distinct("catalogId")
        catalogidcount={}
        catalogid=[]
        for x in result:
            if(type(x) is str and x!="undefined" and x[-1]!="."):
                catalogid.append(x)
                # mycursor = mydb1.cursor()     
                y=mycol.count_documents({ 
                    "event_type": "open_catalog",
                    "catalogId": x ,
                    "dealerId":str(self.dealerid)
                }) 
                catalogidcount[x]=y
        Key_max = max(zip(catalogidcount.values(), catalogidcount.keys()))[1]  
        myresult = ob.catalogname_with_dealer(Key_max, self.dealerid)
        return myresult
    
    def highest_selling_product(self):
        productids=[]
        productcount=mycol.count_documents({"event_type": "get_quote", "dealerId":self.dealerid}) 
        if(productcount>0):
            for x in mycol.find():
                if(x.get('dealerId')==self.dealerid and x.get('event_type')=='get_quote'):
                    product=x.get('products')
                    for p in product:
                        productids.append(p.get('productId'))   
            occurrence = {item: productids.count(item) for item in productids}  
            Key_max = max(zip(occurrence.values(), occurrence.keys()))[1]  
            for y in mycol3.find():
                if y.get('_id')==ObjectId(Key_max):
                    title = y.get('title')
                    return f"highest selling product is {title}"
        else:
            return "No product sell yet!"
        
    def catalog_impression(self):
        dealercount=mycol.count_documents({"dealerId": self.dealerid}) 
        if(dealercount==0):
            return 'No catalog access.'
        else:
            catalogidcount={}
            for x in mycol.find({"dealerId":self.dealerid}):
                catalogid=x.get("catalogId")
                if(catalogid!="undefined"):
                    y=mycol.count_documents({ 
                            "event_type": {"$in": ["open_catalog", "load_more"]},
                            "catalogId": catalogid,
                            "dealerId":self.dealerid
                        }) 
                    catalogidcount[catalogid]=y
            Key_max = [key for key in catalogidcount if all(catalogidcount[temp] <= catalogidcount[key] for temp in catalogidcount)]
            if(len(Key_max)==1):
                myresult = ob.catalogname_with_dealer(Key_max[0], self.dealerid)
                return f"{myresult} catalog's products access most"
            else:
                catalogdata=[]
                for k in Key_max:
                    myresult = ob.catalogname_with_dealer(k, self.dealerid)
                    catalogdata.append(myresult)
                return f"{catalogdata} products access in equal amount"
    
    def most_running_store(self):
        productids=[]
        storenames=[]
        productcount=mycol.count_documents({"event_type": "get_quote", "dealerId":self.dealerid}) 
        if(productcount>0):
            for x in mycol.find():
                if(x.get('dealerId')==self.dealerid and x.get('event_type')=='get_quote'):
                    product=x.get('products')
                    for p in product:
                        productids.append(p.get('productId'))   
            occurrence = {item: productids.count(item) for item in productids}  
            if(all(x==list (occurrence.values())[0] for x in occurrence.values())==True): 
                for p in productids:
                    for y in mycol3.find():
                        if y.get('_id')==ObjectId(p):    
                            return f"{y.get('store').get('label')} is most running store"
            else:
                Key_max = [key for key in occurrence if all(occurrence[temp] <= occurrence[key] for temp in occurrence)]  
                if(len(Key_max)>1):
                    for k in Key_max:
                        for y in mycol3.find():
                            if y.get('_id')==ObjectId(k):  
                                storenames.append(y.get('store').get('label'))     
                    return storenames
                else:
                    for y in mycol3.find():
                        if y.get('_id')==ObjectId(Key_max[0]):  
                            return f"{y.get('store').get('label')} is most running store" 
        else:
            return "running status of all stores are consistent"
        
    def add_to_cart(self):
        title = []
        for x in mycol.find():
            event_type = x.get("event_type", "N/A")
            dealerId=x.get("dealerId","N/A")
            if(event_type=='add_to_cart' and dealerId==self.dealerid):
                product=x.get("products","N/A")[0].get("productId")    
                for y in mycol3.find():
                    if y.get('_id')==ObjectId(product):
                        title.append(y.get('title'))
        finalTitle = list(set(title))
        return finalTitle
    
    def most_search_keyword(self):
        searchtotal={}
        for x in mycol.find({'filters.searchKeywords':{'$ne':""},'dealerId':self.dealerid}):
            searchKeywords=x.get('filters').get('searchKeywords')
            countsearch=mycol.count_documents({
                'dealerId':self.dealerid,
                'filters.searchKeywords':searchKeywords
            })
            searchtotal[searchKeywords]=countsearch
        if(len(searchtotal)==0):
            return "User applied no search keyword filter."
        else:
            Key_max = [key for key in searchtotal if all(searchtotal[temp] <= searchtotal[key] for temp in searchtotal)]
            if(len(Key_max)==1):
                return f"Most search keyword is {Key_max[0]}"
            else:
                return f"Most search keywords are:- {Key_max}"
            
    def common_search_keywords(self):
        searchtotal={}
        for x in mycol.find({'filters.searchKeywords':{'$ne':""},'dealerId':self.dealerid}):
            searchKeywords=x.get('filters').get('searchKeywords')
            countsearch=mycol.count_documents({
                'dealerId':self.dealerid,
                'filters.searchKeywords':searchKeywords
            })
            searchtotal[searchKeywords]=countsearch
        if(len(searchtotal)==0):
            return "User applied no search keyword filter."
        else:
            ThreeHighest = nlargest(3, searchtotal, key = searchtotal.get) 
            return f"Common search keywords are:- {ThreeHighest}"

    def most_filtered_tag(self):
        alltags=[]
        counttag=mycol.count_documents({
            'dealerId':self.dealerid,
            'filters.marketTags':{'$ne':[]}
        })
        if(counttag>0):
            for x in mycol.find({'dealerId':self.dealerid, 'filters.marketTags':{'$ne': []}}):
                marketTags=x.get('filters').get('marketTags')
                alltags.extend(marketTags)
            d = dict.fromkeys(alltags, 0)
            for val in alltags:
                d[val] += 1
            Key_max = [key for key in d if all(d[temp] <= d[key] for temp in d)]
            if(len(Key_max)==1):
                return f"Most filtered tag is {Key_max[0]}."
            else:
                return f"Most filtered tags are:- {Key_max}"
        else:
            return "No user applied any tag."
        
    def most_filtered_category(self):
        category=[]
        manycategories=[]
        countcategory=mycol.count_documents({
            'dealerId':self.dealerid,
            'filters.categoryIds':{'$ne':[]}
        })
        if(countcategory>0):
            for x in mycol.find({'dealerId':self.dealerid,'filters.categoryIds':{'$ne':[]}}):
                categoryIds=x.get('filters').get('categoryIds')
                category.extend(categoryIds)
            d = dict.fromkeys(category, 0)
            for val in category:
                d[val] += 1
            Key_max = [key for key in d if all(d[temp] <= d[key] for temp in d)]
            if(len(Key_max)==1):
                myresult = ob.category(Key_max[0], self.dealerid)
                return f"Most filtered category is {myresult}"
            else:
                for k in Key_max:
                    myresult = ob.category(k, self.dealerid)
                    manycategories.append(myresult)
                return f"Most filtered categories are:- {manycategories}"
        else:
            return 'No user apply category filter.'



    def top_x_products(self, str2):
        output = list(map(int, re.findall(r'\d+', str2)))
        if(len(output)==0):
            try:
                w2n.word_to_num(str2)
                nproduct = w2n.word_to_num(str2)
            except ValueError:
                return "Please enter your query with number that how many products you want"
        else:
            nproduct = output[0]
        productids = []
        title = []
        productcount = mycol.count_documents({"event_type": "get_quote", "dealerId": self.dealerid})
        if(productcount>0):
            for x in mycol.find():
                if(x.get('dealerId')==self.dealerid and x.get('event_type')=="get_quote"):
                    product = x.get('products')
                    for p in product:
                        productids.append(p.get('productId'))
            occurrence = {item: productids.count(item) for item in productids}
            ThreeHighest = nlargest(nproduct, occurrence, key = occurrence.get)
            for y in mycol3.find():
                for k in ThreeHighest:
                    if y.get('_id')==ObjectId(k):
                        title.append(y.get('title'))
            if(len(occurrence)<nproduct):
                return f"Your only {len(occurrence)} products sell. These are following products sold:- {title}"
            else:
                return title
        else:
            return "No product sell yet!"
    
    # def top_4_products(self):
    #     productids=[]
    #     title=[]
    #     productcount=mycol.count_documents({"event_type": "get_quote", "dealerId":self.dealerid}) 
    #     if(productcount>0):
    #         for x in mycol.find():
    #             if(x.get('dealerId')==self.dealerid and x.get('event_type')=='get_quote'):
    #                 product=x.get('products')
    #                 for p in product:
    #                     productids.append(p.get('productId'))  
    #         occurrence = {item: productids.count(item) for item in productids}  
    #         if(len(occurrence)<4):
    #             Key_max = [key for key in occurrence if all(occurrence[temp] <= occurrence[key] for temp in occurrence)]  
    #             ThreeHighest = nlargest(4, occurrence, key = occurrence.get) 
    #             for y in mycol3.find():
    #                 for k in ThreeHighest:
    #                     if y.get('_id')==ObjectId(k):
    #                         title.append(y.get('title'))
    #             return f"Your only {len(occurrence)} products sell. These are following products sold:- {title}"
    #     else:
    #         return "No product sell yet!"
    
    # def top_5_products(self):
    #     productids=[]
    #     title=[]
    #     productcount=mycol.count_documents({"event_type": "get_quote", "dealerId":self.dealerid}) 
    #     if(productcount>0):
    #         for x in mycol.find():
    #             if(x.get('dealerId')==self.dealerid and x.get('event_type')=='get_quote'):
    #                 product=x.get('products')
    #                 for p in product:
    #                     productids.append(p.get('productId'))  
    #         occurrence = {item: productids.count(item) for item in productids}  
    #         if(len(occurrence)<5):
    #             Key_max = [key for key in occurrence if all(occurrence[temp] <= occurrence[key] for temp in occurrence)]  
    #             ThreeHighest = nlargest(5, occurrence, key = occurrence.get) 
    #             for y in mycol3.find():
    #                 for k in ThreeHighest:
    #                     if y.get('_id')==ObjectId(k):
    #                         title.append(y.get('title'))
    #             return f"Your only {len(occurrence)} products sell. These are following products sold:- {title}"
    #     else:
    #         return "No product sell yet!"

    def most_inquiry(self):
        whatsapp_enquiry=mycol.count_documents({
            'dealerId':self.dealerid,
            "event_type": {"$in": ["whatsapp_enquiry", "share_whatsapp"]}
        })
        get_quote=mycol.count_documents({
            'dealerId':self.dealerid,
            "event_type": "get_quote"
        })
        if(whatsapp_enquiry>get_quote):
            return "User enquires more through whatsapp."
        elif(get_quote>whatsapp_enquiry):
            return "User enquires more through quotation."
        elif(get_quote==0 and whatsapp_enquiry==0):
            return 'No enquiry took place through whatsapp or quotation.'
        else:
            return "Enquiry on whatsapp and through quotation both occur in equal manner."

    def most_viewed_product(self):
        countproduct=mycol.count_documents({
            'event_type':"open_product_detail_page",
            'dealerId':self.dealerid
        })
        title=[]
        products=[]
        if countproduct!=0:
            for x in mycol.find({'dealerId':self.dealerid,'event_type':'open_product_detail_page','products': { '$size': 1}}):
                productids=x.get('products')[0].get('productId')
                products.append(productids)
            occurrence = {item: products.count(item) for item in products} 
            Key_max = [key for key in occurrence if all(occurrence[temp] <= occurrence[key] for temp in occurrence)]
            if(len(Key_max)==1):
                for y in mycol3.find({'dealerId':int(self.dealerid)}):
                    if y.get('_id')==ObjectId(Key_max[0]):
                        title.append(y.get('title'))
            else:
                for y in mycol3.find({'dealerId':int(self.dealerid)}):
                    for k in Key_max:
                        if y.get('_id')==ObjectId(k):
                            title.append(y.get('title'))
            return title
        else:
            return "No product viewed yet!"
        
    def most_user_location(self):
        totalcount=mycol.count_documents({ 
                    "dealerId":self.dealerid
                }) 
        location = []
        if(totalcount==0):
            return "No user accessed your catalog"
        else:
            for x in mycol.find({"dealerId":self.dealerid}):
                location.append(x.get('users').get('userLocation'))
            occurrence = {item: location.count(item) for item in location}
            Key_max = [key for key in occurrence if all(occurrence[temp] <= occurrence[key] for temp in occurrence)] 
            if len(Key_max)>1:
                return f"most users are from {Key_max}"
            else:
                return f"most users are from {Key_max[0]}"
            
    def all_user_location(self):
        totalcount=mycol.count_documents({ 
                    "dealerId":self.dealerid
                }) 
        location = set()
        if(totalcount==0):
            return "No user accessed your catalog"
        else:
            for x in mycol.find({"dealerId":self.dealerid}):
                location.add(x.get('users').get('userLocation'))
            return location
            
    def user_device_type(self):
        totalcount=mycol.count_documents({ 
                    "dealerId":self.dealerid
                }) 
        mobilecount=0
        laptopcount=0
        if(totalcount==0):
            return "No user accessed your catalog"
        else:
            for x in mycol.find({"dealerId":self.dealerid}):
                if(x.get('users').get('deviceType') == 'Mobile'):
                    mobilecount+=1
                else:
                    laptopcount+=1
        if(mobilecount>laptopcount):
            return "Users use mostly use Mobiles to access your catalogs."
        elif(mobilecount<laptopcount):
            return "Users mostly access your catalogs through Laptop/Desktop."
        else:
            return "User access your catalogs with mobile and laptop/desktop in similar manner."
        
    def most_applied_sorting(self):
        sorting = []
        totalcount=mycol.count_documents({
            'dealerId': self.dealerid,
            'event_type': 'apply_filters',
            'filters.PriceSort': {'$ne': None}
        })
        if(totalcount>0):
            for x in mycol.find({'dealerId': self.dealerid,'event_type': 'apply_filters'}):
                if((x.get('filters').get('PriceSort')) is None):
                    pass
                else:
                    sorting.append(x.get('filters').get('PriceSort'))
            occurrence = {item: sorting.count(item) for item in sorting}
            Key_max = [key for key in occurrence if all(occurrence[temp] <= occurrence[key] for temp in occurrence)]
            if(len(Key_max)>1):
                return 'Users applied ascending and descending sorting in similar manner'
            else:
                return f'{Key_max[0]} sorting is mostly applied by users'
        else:
            return 'No user applied any price sorting'
        
    def most_applied_price_range(self):
        price=[]
        for x in mycol.find({'dealerId':self.dealerid,"filters.priceRange":{'$ne':[]}}):
            priceRange=x.get('filters').get('priceRange')
            if(sum(priceRange)!=0):
                price.append(priceRange)
        if(len(price)>0):
            sublist_tuples = [tuple(sublist) for sublist in price]
            counter = Counter(sublist_tuples)
            max_occurrence_sublist = counter.most_common(1)[0][0]
            return f"Maximum time occur price range in catalogs is from {list(max_occurrence_sublist)}"
        else:
            return "No price range filter applied by any user"
        
    def most_viewed_catagory(self):
        countproduct=mycol.count_documents({
            'event_type':"open_product_detail_page",
            'dealerId':self.dealerid
        })
        if(countproduct>0):
            categories=[]
            products=[]
            for x in mycol.find({'dealerId':self.dealerid,'event_type':'open_product_detail_page','products': { '$size': 1}}):
                productids=x.get('products')[0].get('productId')
                products.append(productids)
            occurrence = {item: products.count(item) for item in products} 
            Key_max = [key for key in occurrence if all(occurrence[temp] <= occurrence[key] for temp in occurrence)]
            if(len(Key_max)==0):
                return "No category specify for most viewed product."
            else:
                if(len(Key_max)==1):
                    for x in mycol.find({'dealerId':self.dealerid,'event_type':'open_product_detail_page','products': { '$size': 1},'products.productId':Key_max[0], "products.categoryIds":{'$ne': []}}):
                        if(type(x.get('products')[0].get('categoryIds')[0]) == int):
                            categories.append(x.get('products')[0].get('categoryIds')[0])
                        else:
                            categories.append(x.get('products')[0].get('categoryIds')[0].get('id'))
                else:
                    for k in Key_max:
                        for x in mycol.find({'dealerId':self.dealerid,'event_type':'open_product_detail_page','products': { '$size': 1},'products.productId':k,"products.categoryIds":{'$ne': []}}):
                            if(type(x.get('products')[0].get('categoryIds')[0]) == int):
                                categories.append(x.get('products')[0].get('categoryIds')[0])
                        else:
                            categories.append(x.get('products')[0].get('categoryIds')[0].get('id'))
                categoryoccurrence = {item: categories.count(item) for item in categories} 
                if(len(categoryoccurrence)!=0):
                    categoryKey_max = [key for key in categoryoccurrence if all(categoryoccurrence[temp] <= categoryoccurrence[key] for temp in categoryoccurrence)]
                    myresult = ob.category(categoryKey_max[0], self.dealerid)
                    return myresult[0]
                else:
                    return "No category specify for most viewed product."
        else:
            return 'No product viewed.'

    def most_viewed_tag(self):
        countproduct=mycol.count_documents({
            'event_type':"open_product_detail_page",
            'dealerId':self.dealerid
        })
        if(countproduct>0):
            markettags=[]
            products=[]
            for x in mycol.find({'dealerId':self.dealerid,'event_type':'open_product_detail_page','products': { '$size': 1}}):
                productids=x.get('products')[0].get('productId')
                products.append(productids)
            occurrence = {item: products.count(item) for item in products} 
            Key_max = [key for key in occurrence if all(occurrence[temp] <= occurrence[key] for temp in occurrence)]
            if(len(Key_max)==0):
                return "No tag specify for most viewed product."
            else:
                if(len(Key_max)==1):
                    for x in mycol.find({'dealerId':self.dealerid,'event_type':'open_product_detail_page','products': { '$size': 1},'products.productId':Key_max[0], "products.marketTags":{'$ne': []}}):
                        markettags.extend(x.get('products')[0].get('marketTags'))
                tagoccurrence = {item: markettags.count(item) for item in markettags} 
                tagKey_max = [key for key in tagoccurrence if all(tagoccurrence[temp] <= tagoccurrence[key] for temp in tagoccurrence)]
                if(len(tagKey_max)!=0):
                    return tagKey_max
                else:
                    return 'No tag specify for most viewed product.'
        else:
            return 'No product viewed.'
        
    def most_viewed_price_range(self):
        countproduct=mycol.count_documents({
            'event_type':"open_product_detail_page",
            'dealerId':self.dealerid
        })
        if(countproduct>0):
            price=[]
            products=[]
            for x in mycol.find({'dealerId':self.dealerid,'event_type':'open_product_detail_page','products': { '$size': 1}}):
                productids=x.get('products')[0].get('productId')
                products.append(productids)
            occurrence = {item: products.count(item) for item in products} 
            Key_max = [key for key in occurrence if all(occurrence[temp] <= occurrence[key] for temp in occurrence)]
            if(len(Key_max)==0):
                return "No price specify for most viewed product."
            else:
                if(len(Key_max)==1):
                    for x in mycol.find({'dealerId':self.dealerid,'event_type':'open_product_detail_page','products': { '$size': 1},'products.productId':Key_max[0], "products.marketTags":{'$ne': []}}):
                        price.append(x.get('products')[0].get('price'))
                priceoccurrence = {item: price.count(item) for item in price} 
                priceKey_max = [key for key in priceoccurrence if all(priceoccurrence[temp] <= priceoccurrence[key] for temp in priceoccurrence)]
                if(len(priceKey_max)!=0):
                    return f"Most viewed products of price {priceKey_max}"
                else:
                    return 'No price specify for most viewed product.'
        else:
            return 'No product viewed.'
        
    def most_interesting_product(self):
        y=mycol.count_documents({ 
                    "event_type": {"$in": ["open_product_detail_page", "view_gallery"]},
                    "dealerId":self.dealerid
                }) 
        if(y>0):
            productids=[]
            title=[]
            for x in mycol.find({"dealerId":self.dealerid, "event_type": {"$in": ["open_product_detail_page", "view_gallery"]},'products':{'$size':1}}):
                product=x.get('products')[0].get('productId')
                productids.append(product)
            occurrence = {item: productids.count(item) for item in productids} 
            Key_max = [key for key in occurrence if all(occurrence[temp] <= occurrence[key] for temp in occurrence)]
            if(len(Key_max)==1):
                for y in mycol3.find({'dealerId':int(self.dealerid)}):
                    if y.get('_id')==ObjectId(Key_max[0]):
                        title.append(y.get('title'))
                return title
            elif(len(Key_max)>1):
                for y in mycol3.find({'dealerId':int(self.dealerid)}):
                    for k in Key_max:
                        if y.get('_id')==ObjectId(k):
                            title.append(y.get('title'))
                return title
            else:
                return "No product appear as interesting product!"
        else:
            return "No product appear as interesting product!"