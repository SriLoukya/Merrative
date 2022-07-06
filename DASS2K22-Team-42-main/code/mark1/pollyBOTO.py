from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os

session = Session(profile_name="IAMadmin")
polly = session.client("polly")

text = "This is a proof of concept that we can reach Amazon's Polly servers"

try:
    response = polly.synthesize_speech(Text=text, OutputFormat="ogg_vorbis", VoiceId="Hans")
except (BotoCoreError, ClientError) as error:
    print(error)
    quit(-1)

if "AudioStream" in response:
    with closing(response["AudioStream"]) as stream:
        output = "speech.ogg"
        try:
            with open(output, "wb") as file:
                file.write(stream.read())
        except IOError as error:
            print(error)
            quit(-1)
else:
    print("Could not stream audio")
    quit(-1)

os.system("xdg-open " + output)
