import psycopg2
import time
import pandas as pd
import numpy as np
import requests
import json
import csv
from parameters import paras
import re

def _makelist(uniresponsedict): #Takes dictionary from universalis listing and breaks down information of each listing
    response_dict = uniresponsedict
    for num, item in enumerate(response_dict['listings']):
        item_id = response_dict['itemID']
        # last_upload_time = response_dict['lastUploadTime']
        world_id = response_dict['worldID']
        dc_name = "crystal"
        world_name = 'lookup'
        post_time = response_dict['listings'][num]['lastReviewTime']
        price_per_unit = response_dict['listings'][num]['pricePerUnit']
        quantity = response_dict['listings'][num]['quantity']
        creator_name = response_dict['listings'][num]['creatorName']
        hq = response_dict['listings'][num]['hq']
        crafted = response_dict['listings'][num]['isCrafted']
        retainer_name = response_dict['listings'][num]['retainerName']
        total = response_dict['listings'][num]['total']
        print(num, item_id, world_id, dc_name, world_name, post_time, price_per_unit, quantity, creator_name,
         hq, crafted, retainer_name, total)



class CoeurlConnection:
    def __init__(self, user="guest", paras=None):
        self.paras = paras
        self.user = user
        if paras:
            self.password = self.paras["users"][user]
        else:
            self.user = "guest"
        self._setconn()

    def _setconn(self):
        if self.paras != None:
            self.conn = psycopg2.connect("dbname=coeurlation user={} password={}".format(self.user, self.password))
        if self.paras == None: 
            self.conn = psycopg2.connect("dbname=coeurlation user=guest")
        self.conn.set_client_encoding('UTF8')
        self.cursor = self.conn.cursor()
        

    def _execute(self,string):
        self.cursor.execute(string)
        data = self.cursor.fetchall()
        data = pd.DataFrame(data)
        self.conn.close()
        return data


class UniQuery:
    def __init__(self, worldids, itemids, querytype="currentlistings"):
        self.targetworlds = [worldids]
        self.targetids = ",".join(itemids)
        self.url = 'https://universalis.app/api/'
        if querytype = "currentlistings":
            
        pass
            
    #Takes url for API and converts the json string into a python dictionary.
    def _retrieve(url):
        response = requests.get(url)
        status_code = response.status_code
        response_file = response.content
        response_dict = json.loads(response_file)
        return response_dict

    #Takes dictionary from _retrieve called on looking at current market board listings and outputs cleaned dataframe.
def _currenttodf(currenturl):
    data = _retrieve(currenturl)
    extract = []
    for item in data["items"]:
        itemid = item["itemID"]
        worldid = item["worldID"]
        worldname = item["worldName"]
        lastuploadtime = item["lastUploadTime"]
        for listing in item["listings"]:
            rowdict = {"itemID":itemid, "worldID":worldid, "worldName":worldname}
            
            for x in listing:
                var = str(x)
            
                rowdict[var] = listing[var]
            print(rowdict)
            extract.append(rowdict)
        df = pd.DataFrame(extract)
        df = df.drop(labels=["retainerID",'materia','onMannequin','stainID','creatorName'], axis=1)
        print(df)
        return df

# servers = ['Balmung', 'Brynhildr', 'Coeurl', 'Diabolos', 'Goblin', 'Malboro', 'Mateus', 'Zalera']


# _currenttodf()
# #pd.DataFrame.to_sql(listings, conn, if_exists = 'append')
