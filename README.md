# Flask API

Use the REST API to create calls to get the data you need to analyze and query advertising data. The advertising data is from our RTB (Real-Time-Biding) department.
The general RTB flow is:
1. User opens an app with placements for ads.
2. An ad request with the placement and user details is sent to potential buyers.
3. An auction starts and the buyer with the highest bid wins.
4. The winning buyer displays his ad to the user (this is an impression).
5. The user sees the ad and may click on it.

# Requirements:
-   Python 3.8
-   Flask 1.1.+

# Import
from flask import Flask, json, request  
from werkzeug.serving import WSGIRequestHandler  
import pandas as pd

# Files

### requests.csv:
timestamp: Linux epoch timestamp
session_id: unique identifier for session_id
partner: partner name
user_id: unique identifier for user
bid: a float value represents the price
win: a Boolean value shows if the bid won

### impressions.csv:
timestamp: Linux epoch timestamp
session_id: unique identifier for session_id
Duration: impressions duration time

### clicks.csv:
timestamp: Linux epoch timestamp
session_id: unique identifier for session_id
Time: time passed till the user click the ad.


## Running the app

### Now run the webapp:
$ python rest_api.py
 * Running on http://127.0.0.1:5000/

### You can now open a new tab and interact with the API from the command line:

### /keepalive:
Input: None
Output: is the service up and ready for query

### /userStats
Input: user_id
Output:

Num of requests

Num of impressions

Num of clikcs

Average price for bid (include only wins)

Median Impression duration

Max time passed till click

### /sessionId
Input: session_id
Output:

Begin: request timestamp

Finish: latest timestamp (request/click/impression)

Partner name
