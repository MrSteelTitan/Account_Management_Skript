import json
import pandas as pd
from pymongo import MongoClient
import firebase_admin
from firebase_admin import credentials

def startup():
    with open('config.json') as json_file:
        config = json.load(json_file)

        cluster = MongoClient(config['config']['mongodb']['uri'])
        db = cluster[config['config']['mongodb']['cluster']]
        collection = db[config['config']['mongodb']['collection']]

        cred = credentials.Certificate(config['config']['firebase'])
        firebase_admin.initialize_app(cred)

        df = pd.read_excel(config['config']['excel'], header=0, index_col=None)

        config['config']['mongodb']['uri']

        return collection, cred, df


print(startup())
