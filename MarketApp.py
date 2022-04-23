from parameters import paras
import io
from timeit import timeit
from matplotlib.style import use
import psycopg2
import time
import os
import pandas as pd
import numpy as np
from pytz import timezone
import requests
import json
import csv
# from parameters import paras
import re
import pandasgui
from sqlalchemy import asc, true

database = 'coeurlation'

connect = psycopg2.connect(database='coeurlation', user='bbbot', password=paras['users']['bbbot'])


def timefunction(func):
    print('Starting process')
    start = time.time()
    to_return = func
    finish = time.time()
    print(f'time elapsed: {finish - start}')

    return to_return

#holds login information for our database and facilitates queries to it.
# class CoeurlConnection:
#     def __init__(self, user="bbbot", paras=None):
#         self.paras = paras
#         self.user = user
#         if paras:
#             self.password = self.paras["users"][user]
#         else:
#             self.user = "bbbot"
#             self.password = "bbbotpassword"
#         if self.paras != None:
#             self.password = paras["users"][user]
#             self.conn = psycopg2.connect("dbname=coeurlation user={} password={}".format(self.user, self.password))
#         if self.paras == None: 
#             self.conn = psycopg2.connect("dbname=coeurlation user=bbbot password=bbbotpassword")
        # self.conn.set_client_encoding('UTF8')
        # self.cursor = self.conn.cursor()

    
    ##takes list of itemids and returns dfs with item names and ids
def finditemname(conn, itemids):
    # self._setconn()
    with conn.cursor() as cursor:
        cursor.execute("select * from itemlist where itemid in %s;", (tuple([int(itemid) for itemid in itemids]),))
            # data = data[data['itemid']).contains(id, case=False,na=None,regex=False)]
        data = cursor.fetchall()
        data = pd.DataFrame(data,columns = ['itemname','itemid'])
        data.set_index('itemid', inplace=True)

    return data

def itemlookup(conn,itemname):
    with conn.cursor() as cursor:
        cursor.execute("select * from itemlist where lower(itemname) like %s", ("%" + itemname.lower() + "%",))
        data = cursor.fetchall()
        data = pd.DataFrame(data, columns = ['itemname', 'itemid'])
        data.set_index('itemid', inplace=True)
        return data


    



#Formats url to acquire json from universalis and parses the information into dataframes.
class UniQuery:
    def __init__(self, dbconn, worldnames, itemids, querytype='currentlistings', add=None):
        self.targetworlds = worldnames.replace(" ", "").split(',')
        self.targetids = itemids.replace(" ", "").split(',')
        self.add = add
        # if dbconn:
        #     self.db=dbconn
        # else:
        #     self.db = CoeurlConnection()
        self.ilist = finditemname(connect,self.targetids)
        self.targetids = '%2c'.join(self.targetids)
        self.url = 'https://universalis.app/api/'
        

        # if worldname in servers:
        if querytype == "salehistory":
            self.df = self._historytodf()
        

        if querytype == "currentlistings":
            self.df = self._currenttodf()
            
            
 #Takes url for API and converts the json string into a python dictionary.
    def _retrieve(self):
        response = requests.get(self.url)
        status_code = response.status_code
        response_file = response.content
        response_dict = json.loads(response_file)
        return response_dict

        #Takes dictionary from _retrieve called on looking at current market board listings and outputs cleaned dataframe.
    def _currenttodf(self):
        extract = []
        for world in self.targetworlds:
            self.url = 'https://universalis.app/api/' + world + '/' + self.targetids
            if self.add:
                self.url += self.add
            data = self._retrieve()
            if "itemIDs" in data:
                for item in data['items']:
                    itemid = item['itemID']
                    itemname = self.ilist[self.ilist.index == itemid].values[0][0]
                    # itemname = self.ilist['itemname'].values[self.ilist['itemid'] == itemid]
                    worldid = item["worldID"]
                    worldname = item["worldName"]
                    lastuploadtime = item["lastUploadTime"]
                    for listing in item["listings"]:
                        realtime = time.ctime(listing['lastReviewTime'])
                        rowdict = {"itemID":itemid,"itemName":itemname,"worldID":worldid, "worldName":worldname,"lastUploadTime":lastuploadtime, "postedAt":realtime}
                    
                        for x in listing:
                            var = str(x)
                            rowdict[var] = listing[var]
                        extract.append(rowdict)
                
            else:
                itemid = data['itemID']
                worldid = data["worldID"]
                worldname = data["worldName"]
                itemname = self.ilist[self.ilist.index == itemid].values[0][0]
                # for row in self.ilist:
                #         if int(itemid) in row['itemid'].values:
                #             itemname = row['itemname'].values[0]
                lastuploadtime = data["lastUploadTime"]
                for listing in data["listings"]:
                    realtime = time.ctime(listing['lastReviewTime'])
                    rowdict = {"itemID":itemid,"itemName":itemname,"worldID":worldid, "worldName":worldname,"lastUploadTime":lastuploadtime, "postedAt":realtime}
                    
                    for x in listing:
                        var = str(x)
                        rowdict[var] = listing[var]
                    extract.append(rowdict)
        
        df = pd.DataFrame(extract)
        # df = df.drop(labels=["retainerID",'materia','onMannequin','stainID','creatorName'], axis=1)
        df = df[['itemName','worldName','itemID','worldID',
                'postedAt','pricePerUnit', 'quantity', 'total',
                'creatorID','listingID', 'hq', 'isCrafted', 
                'retainerCity', 'retainerName','lastUploadTime','lastReviewTime', 'sellerID']]
        
        
        # df = df[['lastreviewtime','itemID','worldID', 'worldName','itemname','iscrafted', 'creatorID','hq','listingID','retainerName','sellerID','quantity','total']]
        return df

#intakes sale history for listed world(s) and creates dataframe.
    def _historytodf(self):
        extract = []
        for world in self.targetworlds:
            self.url = 'https://universalis.app/api/' +'history/' + world + '/' + self.targetids
            if self.add:
                self.url += self.add
            data = self._retrieve()
            if 'itemIDs' in data:
                for item in data["items"]:
                    itemid = item["itemID"]
                    worldid = item["worldID"]
                    worldname = item["worldName"]
                    itemname = self.ilist[self.ilist.index == itemid].values[0][0]
                    lastuploadtime = item["lastUploadTime"]
                    for entry in item["entries"]:
                        realtime = time.ctime(entry['timestamp'])
                        rowdict = {"worldID":worldid,"itemID":itemid,"worldName": worldname,"itemName":itemname,'soldAt':realtime}
                        
                        for x in entry:
                            var = str(x)
                        
                            rowdict[var] = entry[var]
                        extract.append(rowdict)
            else:
                itemid = data["itemID"]
                worldid = data["worldID"]
                worldname = data["worldName"]
                itemname = self.ilist[self.ilist.index == itemid].values[0:]
                lastuploadtime = data["lastUploadTime"]
                for entry in data["entries"]:
                    realtime = time.ctime(entry['timestamp'])
                    rowdict = {"worldID":worldid,"itemID":itemid,"worldName": worldname,"itemName":itemname, 'soldAt': realtime}
                    
                    for x in entry:
                        var = str(x)
                    
                        rowdict[var] = entry[var]
                    extract.append(rowdict)
                    
        df = pd.DataFrame(extract)
        return df


# _currenttodf()
# #pd.DataFrame.to_sql(listings, conn, if_exists = 'append')
# print(bot.df)
# import dataframe_image as dfi
# # pandasgui.show(bot.df)

# df = theDB.itemlookup('materia')

# with io.BytesIO() as temp:
#     dfi.export(df,temp, max_rows = -1)
#     temp.seek(0)
#     print(type(temp))
