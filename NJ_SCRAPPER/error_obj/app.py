from flask import Flask, jsonify
import json
from datetime import datetime, date, time
app = Flask(__name__)



@app.route('/NJ_SCRAPPER/api/v1.0/error/details', methods=['GET'])
def get_tasks():
    d = datetime.now() 
    with open('ticket_details.json') as data_file:
        data = json.loads(data_file.read())
    return jsonify({"Request":'http',"Response":"Api response","Timestamp":d,"Response content":data})


if __name__ == '__main__':
    app.run(host="ec2-52-26-212-108.us-west-2.compute.amazonaws.com",
        port=4321)


