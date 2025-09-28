from networksecurity.exception.exception import NetworkSecurityException
from datetime import datetime
from networksecurity.logging.logger import logging
import os
from typing import List
import pymongo
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from networksecurity.entity.config_entity import DataIngestionConfig
from sklearn.model_selection import train_test_split
from networksecurity.entity.artifact_entity import DataIngestionArtifact

from dotenv import load_dotenv
load_dotenv()

#connected the url of mongo dbs
MONGO_DB_URL=os.getenv("MONGO_DB_URL")


class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_injestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException (e,sys)
        
        
    #this function is responsible for READING  the data from mongofb
    def export_collection_as_dataframe(self):
        try:
            database_name=self.data_injestion_config.database_name

            collection_name=self.data_injestion_config.collection_name
            #creating a mongodb client to interact with database
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name]
            
            #droping the "id" column from list of collection 
            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1)
            
            df.replace("na", np.nan, inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

        
    def export_data_as_feature_store(self,dataframe:pd.DataFrame):
        try:
            #full path where we want to save the raw data 
            feature_store_file_path=self.data_injestion_config.feature_store_file_path
            #creating folder directory 
            dir_path=os.path.dirname(feature_store_file_path)

            #checking it exists or not
            os.makedirs(dir_path,exist_ok=True)

            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def data_as_train_test_split(self,dataframe:pd.DataFrame):
        try:
            #spliiting the data into train test
            train_set,test_set= train_test_split(
                dataframe, test_size=self.data_injestion_config.train_test_split_ratio
            )
            logging.info("splitting train test split")

            #creating dir of folder 
            dir_path=os.path.dirname(self.data_injestion_config.training_file_path)
            logging.info("exited training and testing  of  data ingestion class")

            #checking if its exist or not
            os.makedirs(dir_path,exist_ok=True)
                    
            #converting the training file into csv 

            train_set.to_csv(
            self.data_injestion_config.training_file_path, index=False, header=True
            ) 

            #converting the testing file into csv 
            test_set.to_csv(
                self.data_injestion_config.test_file_path , index=False,header=True
            )
            logging.info(f"Exported train and test file path.")
                
                
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def initiate_data_ingestion(self):
        try:
             #exporting from mongodb

            dataframe=self.export_collection_as_dataframe()

            #saving as feature store raw csv using same variable name dataframe
            dataframe=self.export_data_as_feature_store(dataframe)

            #splitting the train test ratio

            self.data_as_train_test_split(dataframe)
            dataingestionartifact=DataIngestionArtifact(trained_file_path=self.data_injestion_config.training_file_path,
                                                        test_file_path=self.data_injestion_config.test_file_path)
            return dataingestionartifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)


 