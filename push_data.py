import os
import sys
from dotenv import load_dotenv
load_dotenv()

import pymongo

#will search for the mongodb url variable in environment
MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca=certifi.where()


import pandas as pd
import numpy as np
from networksecurity.exception.exception import  NetworkSecurityException
from networksecurity.logging.logger import logging


class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    # this function is responsible for converting the data csv to json
    def csv_to_json_converter(self,file_path):
        data=pd.read_csv(file_path)
        data.reset_index(drop= True,inplace=True)
        records=data.to_dict('records')
        return records
    
    #inserting the data into mongo db
    def insert_data_to_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records
           
            #creating a client which will connect o mongodb
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            self.database=self.mongo_client[self.database]
            
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return (len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
if __name__=='__main__':
        File_path="Network_data\phisingData.csv"
        DATABASE="ibrahim"
        collection="NetworkData"

        networkobj=NetworkDataExtract()
        records=networkobj.csv_to_json_converter(file_path=File_path)
        print(records)
        no_of_records=networkobj.insert_data_to_mongodb(records,DATABASE,collection)
        print(no_of_records)

