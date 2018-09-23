import json
import os
from watson_developer_cloud import TextToSpeechV1

def getWatsonKeys():
    data = json.load(open('keys/ibmwatson.json', 'r'))
    return data["textToSpeech"]["credentials"]

class WatsonTextToSpeech:
    def __init__(self):
        keys = getWatsonKeys()
        self.service = TextToSpeechV1(url=keys['url'], iam_apikey=keys["apikey"])
    def getAudio(self, text):
        response = self.service.synthesize(text, accept='audio/wav', voice="en-US_AllisonVoice")
        return response
    def playAudio(self, text):
        with open('output.wav', 'wb') as audio_file:
            audio_file.write( getAudio(text))
        print('[Checkpoint] Speaking: ', tedt)
        os.system('play output.wav')
