import requests, os, time
from reachAWS import AWSparams

S3bucketName = 'testing42'

text = "This is a third version of the api call. Here, we use StartSpeechSynthesisTask instead of SynthesizeSpeech due to the size restrictions."

method = 'POST'
service = 'polly'
uri = '/v1/synthesisTasks'

request_parameters = '''
    {
        "Engine"                : "standard",
        "LanguageCode"          : "en-IN",
        "OutputFormat"          : "ogg_vorbis",
        "OutputS3BucketName"    : "''' + S3bucketName + '''",
        "Text"                  : "''' + text + '''",
        "TextType"              : "text",
        "VoiceId"               : "Amy"
    }
'''

endpoint, headers = AWSparams( method, '', service, uri, request_parameters, '' )

print('Request URL = ' + endpoint)

response = requests.post( endpoint, data=request_parameters, headers=headers )

print( f"Response code: {response.status_code}\n" )

task = response.json()
outputURI = None
if "SynthesisTask" in task :
    outputURI = task["SynthesisTask"]["OutputUri"]
    status = task["SynthesisTask"]["TaskStatus"]

    if outputURI == None :
        print("could not retrive outputURI")
        print(task)
        quit(-1)

    print(outputURI)
    print(status)
else :
    print("could not do task")
    print(task)
    quit(-1)

print()
print()
print()


######


prefix = "https://s3.ap-south-1.amazonaws.com/testing42"
key = outputURI.removeprefix(prefix)
print( f"getting file: {key}\n" )

method = 'GET'
preservice = S3bucketName + '.'
service = 's3'
uri = key

request_parameters = ''

endpoint, headers = AWSparams( method, preservice, service, uri, '', request_parameters )

print( f'Request URL = {endpoint}\n' )

while True :
    response = requests.get( endpoint, data=request_parameters, headers=headers )
    if response.status_code != 404 :
        break
    print(type(response.status_code), response.status_code)
    time.sleep(1)

print( f"Response code: {response.status_code}\n" )

output = "speech.ogg"
try:
    with open(output, "wb") as file:
        file.write(response.content)
except IOError as error:
    print(error)
    quit(-1)

os.system("xdg-open " + output)

