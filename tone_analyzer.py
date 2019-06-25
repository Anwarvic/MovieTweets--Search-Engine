import json
from utils import *
from tqdm import tqdm
from ibm_watson import ToneAnalyzerV3
from joblib import Parallel, delayed





class IBM_ToneAnalyzer():
	"""Class for calling IBM Tone Analyzer API"""
	def __init__(self):
		# credentials to access Tone Analyzer API 
		cred = parse_yaml('conf.yaml')
		API_KEY = cred['ibm_api_key']
		URL = cred['ibm_url']
		self.api = ToneAnalyzerV3(version=get_todays_date(),
								 iam_apikey=API_KEY,
								 url=URL
								)


	def __get_tone(self, tweet_text):
		# try:
		response = self.api.tone({'text': tweet_text},content_type='application/json')
		result = response.get_result()
		tones = result['document_tone']['tones']
		output = {}
		for tone in tones:
			output[tone['tone_name']] = tone['score']
		return output
		# except:
		# 	return json.dumps("")


	def get_tweets_tone(self, tweets):
		"""
		This method takes a list of tweet ids and returns a list of 
		text within these tweets using parallel programming
		Args:
			ids (list): list of tweet ids taken from raw data
		Returns:
			list of tweet texts.
		"""
		result = Parallel(n_jobs=4, backend="threading")(
            delayed(self.__get_tone)(tw) \
			    for tw in tqdm(tweets, desc="Predicting Tones"))
		return result



if __name__ == "__main__":
	ta = IBM_ToneAnalyzer()
	text = 'I rated Superbad 7/10  #IMDb http://t.co/bk5E1fLOxBx'
	print(ta.get_tweets_tone([text]))