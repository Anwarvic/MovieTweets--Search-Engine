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

	def __get_tweet_by_id(self, tweet_id):
		"""
		This function is responsible for calling twitter API and retireve 
		tweets from based on the tweet_id
		Args:
			tweet_id (int): the id of the tweet to be retrieved using API
		Returns:
			either the tweet content (full text) or an empty string
		"""
		try:
			return self.api.get_status(tweet_id, tweet_mode='extended').full_text
		except:
			return "" # Not Found

	def get_tweets(self, ids):
		"""
		This method takes a list of tweet ids and returns a list of 
		text within these tweets using parallel programming
		Args:
			ids (list): list of tweet ids taken from raw data
		Returns:
			list of tweet texts.
		"""
		result = Parallel(n_jobs=4, backend="threading")(
						delayed(self.__get_tweet_by_id)(id_) \
							for id_ in tqdm(ids, desc="Retrieving Tweets"))
		return result


if __name__ == "__main__":
	t = TwitterCaller()
	tweet_id = 421000000000000000
	print(t.get_tweets([tweet_id]))