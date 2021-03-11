import requests

url = 'https://api.example.com/api/dir/v1/accounts/9999999/orders'
headers = {'Content-Type' : 'application/json'}
r = requests.post(url, data=open('./sampleFile.json', 'rb'), headers=headers)

"""DEV NOTES
json files are too big to be send over http in one go
Possible solutions:
    break down file in pieces
    preprocess to only include transcript and don't use start and end time of each individual word => smaller
"""