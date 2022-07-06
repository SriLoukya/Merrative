import sys, os, datetime, hashlib, hmac, requests
from helpers import getSignatureKey

text = "This is a third version of the api call. Here, we use StartSpeechSynthesisTask instead of SynthesizeSpeech due to the size restrictions."

method = 'POST'
service = 'polly'
host = 'polly.ap-south-1.amazonaws.com'
region = 'ap-south-1'
endpoint = 'https://polly.ap-south-1.amazonaws.com/v1/synthesisTasks'
content_type = 'application/json'

request_parameters = '''
    {
        "Engine"                : "standard",
        "LanguageCode"          : "en-IN",
        "OutputFormat"          : "ogg_vorbis",
        "OutputS3BucketName"    : "testing42",
        "Text"                  : "''' + text + '''",
        "TextType"              : "text",
        "VoiceId"               : "Amy"
    }
'''

access_key = os.environ.get('AWS_ACCESS_KEY_ID')
secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
if access_key is None or secret_key is None:
    print('please add access keys to the env')
    sys.exit()


t = datetime.datetime.utcnow()
amz_date = t.strftime('%Y%m%dT%H%M%SZ')
date_stamp = t.strftime('%Y%m%d')


canonical_uri = '/v1/synthesisTasks'
canonical_querystring = ''
canonical_headers = 'content-type:' + content_type    + '\n' \
                  + 'host:'         + host            + '\n' \
                  + 'x-amz-date:'   + amz_date        + '\n'

signed_headers = 'content-type;host;x-amz-date'

payload_hash = hashlib.sha256(request_parameters.encode('utf-8')).hexdigest()

canonical_request = method                    + '\n' \
                  + canonical_uri             + '\n' \
                  + canonical_querystring     + '\n' \
                  + canonical_headers         + '\n' \
                  + signed_headers            + '\n' \
                  + payload_hash


algorithm = 'AWS4-HMAC-SHA256'
credential_scope = date_stamp + '/' + region + '/' + service + '/' + 'aws4_request'
string_to_sign = algorithm + '\n' \
               +  amz_date + '\n' \
               +  credential_scope + '\n' \
               +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

signing_key = getSignatureKey(secret_key, date_stamp, region, service)
signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()


authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature

headers = {
    'Content-Type'  : content_type,
    'X-Amz-Date'    : amz_date,
    'Authorization' : authorization_header
}

print('Request URL = ' + endpoint)

response = requests.post(endpoint, data=request_parameters, headers=headers)

print('Response code: %d\n' % response.status_code)

task = response.json()
if "SynthesisTask" in task :
    outputURI = task["SynthesisTask"]["OutputUri"]
    status = task["SynthesisTask"]["TaskStatus"]

    print(outputURI)
    print(status)
else :
    print(task)
    print("could not do task")
    quit(-1)
