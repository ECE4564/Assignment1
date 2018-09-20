import json

def getWatsonKeys():
    data = json.load(open('ibmwatson.json', 'r'))
    return data["textToSpeech"]
