import urllib.request
import json
import time
import os

print("How many items should I check? (Defaut 100)")
itemCheckCount = input()
print("How many orders per item should I check? (Default 100)")
statCheckCount = input()

store_list = []
stat_list = []
flip_list = []

stat_count = 0

raw_list = urllib.request.urlopen('https://api.warframe.market/v1/items').read()
json_list = json.loads(raw_list)
urls = json_list['payload']['items']

#print("==============CREATING FLIP LIST==============", file=open("GROFIT.txt", "a"))
print("==============CREATING FLIP LIST==============")

item_count = 0
for item in urls:
    store_details = {"url_name":None, "item_name":None}
    store_details['url_name'] = item['url_name']
    store_details["item_name"] = item["item_name"]
    store_list = []
    if item_count >= int(itemCheckCount):
        break
    item_count += 1
    store_list.append(store_details)
    for name in store_list:
        stat_count = 0
        print(item["item_name"])
        lname = item["item_name"]
        raw_item = urllib.request.urlopen('https://api.warframe.market/v1/items/' + item['url_name'] +'/orders').read()
        json_item = json.loads(raw_item)
        
        plat_item = json_item['payload']['orders']
        
        TopPrice = 0
        BottomPrice = 999999999
        bestBuy = ""
        bestSell = ""
        buyName = ""
        sellName = ""
        for stat in plat_item:
            if True:
                stat_details = {"id":None, "platinum":None, "status":None, "order_type":None}
                stat_details["id"] = stat["id"]
                stat_details["platinum"] = stat["platinum"]
                stat_details["status"] = stat['user']['status']
                stat_details["ingame_name"] = stat['user']["ingame_name"]
                #stat_details["wa_price"] = stat["wa_price"]
                #stat_details["median"] = stat["median"]
                stat_details["order_type"] = stat["order_type"]
                stat_list = []
                stat_list.append(stat_details)
                
                for info in stat_list:
                    #print(info)
                    if stat_count >= int(statCheckCount):
                        break
                    stat_count += 1
                    
                    if stat_details["status"] != "ingame":
                        break
                    
                    
                    if stat['order_type'] == 'buy':
                        #print('buy')
                        if TopPrice < stat["platinum"]:
                            TopPrice = stat["platinum"]
                            bestBuy = str(stat["id"])
                            buyName = stat_details["ingame_name"]
                            
                            

                    if stat['order_type'] == 'sell':
                        #print('sell')
                        if BottomPrice > stat["platinum"]:
                            BottomPrice = stat["platinum"]
                            bestSell = str(stat["id"])
                            sellName = stat_details["ingame_name"]
                    time.sleep(0)
                    

       # if TopPrice != 0:
        #    print("Max Buy is " + str(TopPrice) + " with id " + bestBuy)
       # else:
        #    print("No one is buying this item in the top " + statCheckCount + " orders")

        #if BottomPrice != 999999999:
         #   print("Min Sell is " + str(BottomPrice) + " with id " + bestSell)
        #else:
         #   print("No one is selling this item in the top " + statCheckCount + " orders")
        
        
        if TopPrice > BottomPrice:
            GROFIT = TopPrice - BottomPrice
            flip_list.append((GROFIT, lname, buyName, str(TopPrice), sellName, str(BottomPrice)))
            #print("Pre-sort: " + str(flip_list))
            flip_list.sort(key=lambda profit: profit[0], reverse=True)
            #print("Sorted: " + str(flip_list))
            print("\n", "==============Flip List==============\n", file=open("GROFIT.txt", "a"))
            os.remove("GROFIT.txt")
           # for i in flip_list:
            print("\n", "==============Flip List==============\n")
            print("\n", "==============Flip List==============\n", file=open("GROFIT.txt", "a"))
            for a, b, c, d, e, f in flip_list:
                
                print("\n", "============================\n", "Profit is ", a," platinum.\n\n", b, "\n\n", "Buyer Name is ", c, " at ", d, " platinum.\n", "Seller Name is ", e," at ", f, " platinum.\n", "============================", file=open("GROFIT.txt", "a"))
                print("\n" + "============================\n" + "Profit is " + str(a) + " platinum.\n\n" + str(b) + "\n\n" + "Buyer Name is " + str(c) + " at " + str(d) + " platinum.\n" + "Seller Name is " + str(e) + " at " + str(f) + " platinum.\n" + "============================")
                #with open("GROFIT.txt", "w") as f:
                    #f.write("\n" + "============================\n" + "Profit is " + str(a) + " platinum.\n\n" + str(b) + "\n\n" + "Buyer Name is " + str(c) + " at " + str(d) + " platinum.\n" + "Seller Name is " + str(e) + " at " + str(f) + " platinum.\n" + "============================")

                '''
            print("")
            print("")
            print("============================")
            print(lname)
            print("")
            print("Profit is " + str(GROFIT) + " platinum.")
            print("")
            print("Buyer Name is " + buyName + " at " + str(TopPrice) + " platinum.")
            print("Seller Name is " + sellName + " at " + str(BottomPrice) + " platinum.")
            print("============================")
            print("")
            '''
print("Completed Assigned Flip Check", file=open("GROFIT.txt", "a"))
print("Completed Assigned Flip Check")
