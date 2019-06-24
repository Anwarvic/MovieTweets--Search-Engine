import yaml
import tweepy
from tqdm import tqdm
from joblib import Parallel, delayed



class TwitterCaller():
	"""Class for calling Twitter API"""
	def __init__(self):
		# Variables that contains the user credentials to access Twitter API 
		cred = parse_yaml('conf.yaml')
		ACCESS_TOKEN = cred['twitter_access_token']
		ACCESS_SECRET = cred['twitter_secret_token']
		CONSUMER_KEY = cred['twitter_consumer_key']
		CONSUMER_SECRET = cred['twitter_consumer_secret']
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
		# Create the api to connect to twitter with your creadentials
		self.api = tweepy.API(auth, wait_on_rate_limit=True,
									wait_on_rate_limit_notify=True,
									compression=True)

	