import pymongo

from kafka import KafkaConsumer

import uuid
import datetime
import json

client=pymongo.MongoClient('mongodb+srv://aalferea91:HVPk1tchDKf71SY9@lambdaprojectcluster.epdco1f.mongodb.net/?retryWrites=true&w=majority',tlsAllowInvalidCertificates=True)

social_db=client.social
comments_col=social_db.comments

consumer=KafkaConsumer(
    'social.likes',
    bootstrap_servers=['ec2.fdglkjdnfgamazonwaws.com:9092'])

def process_message(m):
    payload=json.loads(json.loads(m.value)['payload'])
    
    operation=payload['operationType']
    if operation=='insert':
        value=1
    else:
        value=-1
    comment_id=payload['documentKey']['_id'].split('#')[0]
    
    comments_col.update_one(
        {'_id':comment_id},
        {'$inc':{'likes':value}},
         upsert=True
         )

for message in consumer:
    process_message(message)