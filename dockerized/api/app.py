username='aalferea91'
password='HVPk1tchDKf71SY9'
import pymongo
connection = f'mongodb+srv://aalferea91:{password}@lambdaprojectcluster.epdco1f.mongodb.net/?retryWrites=true&w=majority'
client=pymongo.MongoClient(connection)
social_db=client.social
comments_col=social_db.comments
from flask import Flask, jsonify, request
import uuid
import datetime
app = Flask(__name__)
@app.route('/comments',methods=['POST'])
def post_comment():
    body=request.json
    item={
        '_id':str(uuid.uuid4()),
        'created_at':datetime.datetime.utcnow().isoformat(),
        'user':body['user'],
        'text':body['text'],
    }
    comments_col.insert_one(item)
    return jsonify(item)
@app.route('/comments',methods=['GET'])
def get_comments():
    items=list(comments_col.find({}))
    return jsonify(items)
app.run(host='localhost')