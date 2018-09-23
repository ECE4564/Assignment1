import json
import os
from watson_developer_cloud import TextToSpeechV1

def getWatsonKeys():
    data = json.load(open('keys/ibmwatson.json', 'r'))
    return data["textToSpeech"][0]["credentials"]

class WatsonTextToSpeech:
    def __init__(self):
        keys = getWatsonKeys()
        self.service = TextToSpeechV1(url=keys['url'], iam_apikey=keys["apikey"])
        #print(keys["apikey"])
    def getAudio(self, text):
        return self.service.synthesize(text, accept='audio/wav', voice="en-US_AllisonVoice").get_result()
    def playAudio(self, text):
        with open('output.wav', 'wb') as audio_file:
            #print(self.getAudio(text))
            audio_file.write(self.getAudio(text).content)
        #print('[Checkpoint] Speaking: ', tedt)
        os.system('play output.wav')
