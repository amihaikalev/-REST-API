from flask import Flask, json, request
from werkzeug.serving import WSGIRequestHandler

import pandas as pd


api = Flask(__name__)


@api.route('/keepalive', methods=['GET'])
def api_users():
    try:
        requests = pd.read_csv("requests.csv", names=['timestamp', 'session_id', 'partner', 'user_id', 'bid', 'win'])
        impressions = pd.read_csv("impressions.csv", names=['timestamp', 'session_id', 'duration'])
        clicks = pd.read_csv("clicks.csv", names=['timestamp', 'session_id', 'time'])
        return json.dumps("Files loaded successfully")
    except Exception as e:
        # Whoops it wasn't a 200
        return json.dumps("Error: " + str(e))


@api.route("/userStats/<user_id>", methods=['GET'])
def userStats(user_id):
    requests = pd.read_csv("requests.csv", names=['requests_timestamp', 'session_id', 'partner', 'user_id', 'bid', 'win'])
    impressions = pd.read_csv("impressions.csv", names=['impressions_timestamp', 'session_id', 'duration'])
    clicks = pd.read_csv("clicks.csv", names=['clicks_timestamp', 'session_id', 'time'])

    # In each file session_id is unique

    user_dict = {}
    user_request = requests[requests['user_id'] == user_id]
    if len(user_request) == 0:
        return "User Not Found"
    num_of_requests = len(user_request)
    user_dict['num_of_requests'] = num_of_requests
    user_impressions = user_request.merge(impressions, on='session_id', how='inner')
    num_of_impressions = len(user_impressions)
    user_dict['num_of_impressions'] = num_of_impressions
    user_clicks = user_impressions.merge(clicks, on='session_id', how='inner')
    num_of_clicks = len(user_clicks)
    user_dict['num_of_clicks'] = num_of_clicks
    average_price_for_bid = round( user_impressions['bid'].mean() , 2)
    user_dict['average_price_for_bid'] = average_price_for_bid
    median_impression_duration = user_impressions['duration'].median()
    user_dict['median_impression_duration'] = median_impression_duration
    max_time_passed_till_click = user_clicks['time'].max()
    user_dict['max_time_passed_till_click'] = max_time_passed_till_click
    return json.dumps(user_dict)


@api.route("/sessionId/<session_id>", methods=['GET'])
def sessionId(session_id):
    requests = pd.read_csv("requests.csv", names=['requests_timestamp', 'session_id', 'partner', 'user_id', 'bid', 'win'])
    impressions = pd.read_csv("impressions.csv", names=['impressions_timestamp', 'session_id', 'duration'])
    clicks = pd.read_csv("clicks.csv", names=['clicks_timestamp', 'session_id', 'time'])
    
    # In each file session_id is unique

    session_dict = {}
    session_request = requests[ requests['session_id'] == session_id ]
    if len(session_request) == 0:
        return "Session Not Found"
    session_impressions = impressions[ impressions['session_id'] == session_id ]
    session_clicks = clicks[clicks['session_id'] == session_id]
    begin = session_request['requests_timestamp'].iloc[0]
    session_dict['begin'] = int(begin)
    if len(session_clicks)>0:
        finish = 'click and timestamp '+str(session_clicks['clicks_timestamp'].iloc[0])
    elif len(session_impressions)>0:
        finish = 'impressions and timestamp '+str(session_impressions['impressions_timestamp'].iloc[0])
    else:
        finish = 'request and timestamp '+str(session_request['requests_timestamp'].iloc[0])
    session_dict['finish'] = finish
    partner_name = session_request['partner'].iloc[0]
    session_dict['partner_name'] = partner_name
    return json.dumps(session_dict)

if __name__ == '__main__':
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    api.run()
    
