from distutils.log import error
import os
import io

from numpy import copyto
import MarketApp
from MarketApp import *
import pandas
import re
from parameters import paras
import threading


servers = ['Balmung', 'Brynhildr', 'Coeurl', 'Diabolos', 'Goblin', 'Malboro', 'Mateus', 'Zalera']
serverstring = ",".join(servers)

items= []

# bot = UniQuery(worldnames=serverstring, itemids = '6548,7490', querytype='currentlistings',)
theDB = CoeurlConnection(user="postgres", paras= paras)


def insert_listings(worldlist, itemidlist = None, type = 'currentlistings'):
    hq = UniQuery(worldnames=worldlist, itemids = itemidlist, querytype = type)
    hq.df.reset_index(inplace=True)
    hq.df = hq.df[['index', 'itemName', 'worldName', 'itemID', 'worldID', 'postedAt',
       'pricePerUnit', 'quantity', 'total', 'creatorID', 'listingID', 'hq', 'isCrafted',
       'retainerCity', 'retainerName', 'lastUploadTime', 'lastReviewTime',
       'sellerID']]
    tuple_list = []
    for row in hq.df.values:
        itemlist = []
        for item in row:
            itemlist.append(str(item))
        tuple_list.append(tuple(itemlist))
    args_str = ','.join(['%s'] * len(tuple_list))
    print(tuple_list[:5])
    insert = theDB.cursor.mogrify("INSERT INTO listingsraw VALUES {}".format(args_str), tuple_list)
    try:
        theDB.cursor.execute(insert)
        theDB.conn.commit()
        print(f'currentlistings updated for items {itemidlist} on servers {worldlist}')
    except:
        print("error in insert history")
        theDB.conn.rollback()
        theDB.conn.close()
  
insert_listings(servers,)
    
        
    # with io.StringIO() as file:
        
    # # theDB.cursor.execute("INSERT INTO table listingsraw VALUES "+args_str)
    # theDB.conn.commit()


# df = bot.df
# df = df.reset_index()
# df = df.T.drop_duplicates().T
# print(df.values[0])
# value_tuples = ([tuple(row) for row in df.values])



# theDB.cursor.executemany()

# def execute_mogrify(conn, df, table):
    # """
    # Using cursor.mogrify() to build the bulk insert query
    # then cursor.execute() to execute the query
    # """
#     # Create a list of tupples from the dataframe values
#     tuples = [tuple(x) for x in df.values]
#     # Comma-separated dataframe columns
#     cols = ','.join(list(df.columns))
#     # SQL quert to execute
#     cursor = conn.cursor()
#     values = [cursor.mogrify("(%)", tup).decode('utf8') for tup in tuples]
#     query  = "INSERT INTO %s(%s) VALUES " % (table, cols) + ",".join(values)
    
#     try:
#         cursor.execute(query, tuples)
#         conn.commit()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print("Error: %s" % error)
#         conn.rollback()
#         cursor.close()
#         return 1
#     print("execute_mogrify() done")
#     cursor.close()

# execute_mogrify(theDB.conn, bot.df, 'listingraw')

# try:
#     theDB.cursor.execute()
#     theDB.conn.commit()
# except:
#     print('error:%s' % error)
#     theDB.conn.rollback()
#     theDB.cursor.close()
    
# df = bot.df[['worldID', 'worldName', 'itemName', 'hq', 'pricePerUnit', 'quantity', 'soldAt']]
# df = df.sort_values(['itemName','worldID','pricePerUnit'])
