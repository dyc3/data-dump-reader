import requests
import json
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud.tone_analyzer_v3 import ToneInput

watson_api_key = json.load(open("watson_cred.json", "r"))["apikey"]

def get_sentiment(msg):
	# data = {"utterances": []}
	# for m in msg_list:
	# 	data["utterances"] += [{ "text": m.text, "user": m.from_user_id }]

	# resp = requests.post("https://gateway-wdc.watsonplatform.net/tone-analyzer/api/v3/tone?version=2017-09-21", auth=("apikey", watson_api_key), json={"text":msg.text})

	# print(resp)
	# print(resp.text)
	# return resp.json()

	service = ToneAnalyzerV3(
		## url is optional, and defaults to the URL below. Use the correct URL for your region.
		url='https://gateway-wdc.watsonplatform.net/tone-analyzer/api',
		version='2017-09-21',
		iam_apikey=watson_api_key)

	return service.tone(msg.text, "text/plain").get_result()
