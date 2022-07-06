import swagger_client
import base64
import requests
import json
from boto3 import Session

session = Session(profile_name="IAMadmin")
polly = session.client("polly")

access_key = "AKIA4AC4F4NFAQ4WCIDP".encode("UTF-8")
secret_key = "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".encode("UTF-8")

# Header :
'''
POST /v1/synthesisTasks HTTP/1.1
Content-type: application/json
'''

text = "This is a second version of the api call. Here, our aim is to reduce to simple API calls so that we can use them in bubble."

data = {
   "Engine": "standard",
   "LanguageCode": "en-IN",
   "OutputFormat": "ogg_vorbis",
   "OutputS3BucketName": "testingbucket",
   "Text": text,
   "TextType": "text",
   "VoiceId": "Aditi"
}

__CLIENT_ID = '794b2dbb-bd82-4707-a2f7-f3d9899cb386'
__CLIENT_SECRET = 'MzcxNzJhN2UtYjEzNS00MjNjLTg2N2YtMjFlZmRlZWNjMDU1'
__PROTOCOL_HOST_PORT = 'https://<broker-hostname>:8443'

def get_access_token():
    client_credentials = '{client_id}:{client_secret}'.format(client_id=access_key, client_secret=secret_key)
    client_credentials = base64.b64encode(client_credentials.encode('utf-8')).decode('utf-8')
    headers = {
        'Authorization': 'Basic {}'.format(client_credentials),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    endpoint = __PROTOCOL_HOST_PORT + '/oauth2/token?grant_type=client_credentials'
    print('Calling', endpoint, 'using headers', headers)
    res = requests.post(endpoint, headers=headers, verify=True)
    if res.status_code != 200:
        print('Cannot get access token:', res.text)
        return None
    access_token = json.loads(res.text)['access_token']
    print('Access token is', access_token)
    return access_token









try :
    response = requests.post( "https://polly.ap-south-1.amazonaws.com/v1/synthesisTasks", data=data, headers={"Content-Type":"application/json"} )
except IOError as err:
    print(err)
else :
    print(response)
    print(response.content)
    print(response.text)
    print(response.json)
