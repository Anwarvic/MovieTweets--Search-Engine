import json
import random
import pandas as pd
from tqdm import tqdm
from twitter import TwitterCaller
from tone_analyzer import IBM_ToneAnalyzer





def extract_info(data_filepath, movies_filepath):
	"""
	This function reads the test.dat file that contains our data
	and simply extracts four pieces of information:
	- user_id: The user's tweeter account id
	- movie_id: The movie actual id on IMDB
	- rating: The rating on a 10-star scale, extracted from the tweet text
	- tweet_id: The actual tweet
	And it reads movies.dat file and extracts the movie_name based on
	the movie_id
	Args:
		data_filepath (string): the relative/absolute path of test.dat
		movies_filepath (string): the relative/absolute path of movies.dat
	Returns:
		a dataframe written in a csv file
	"""
	# Parse movies.dat
	d = {}
	with open(movies_filepath, 'r', encoding='utf-8') as fin:
		for line in  fin.readlines():
			movie_id, movie_name, _ = line.strip().split("::")
			d[int(movie_id)] = movie_name
	# parse filepath
	with open(data_filepath, 'r') as fin:
		user_ids = []
		movie_ids = []
		movie_names = []
		ratings = []
		tweet_ids = []
		
		for line in tqdm(fin.readlines()[1:10000], desc="Reading Data"):
			lst = line.strip().split(',')
			user_ids.append(int(lst[0]))
			movie_ids.append(int(lst[1]))
			movie_names.append(d[int(lst[1])])
			ratings.append(int(lst[2]))
			# Convert the tweet data string to a JSON object
			json_obj = json.loads(','.join(lst[4:]))
			tweet_ids.append(json_obj['id'])
	
	# save the tweets
	assert len(user_ids) == len(movie_ids) == len(ratings) == len(tweet_ids)
	df = pd.DataFrame.from_dict({"user_id": user_ids,
								 "movie_id": movie_ids,
								 "movie_name": movie_names,
								 "rating": ratings,
								 "tweet_id": tweet_ids})
	df.to_csv('data/MovieTweets1.csv', index=False)


def add_tweet_content(filepath):
	"""
	This function reads the csv produced from the previous function
	extract_info() and gets the tweet ids and use the TwitterCaller()
	class that we have just created to retireve the tweets' content
	Args:
		filepath (string): the relative/absolute path of the csv file
	Returns:
		another csv file containing the tweet text.
	"""
	df = pd.read_csv(filepath, encoding='utf-8')
	obj = TwitterCaller()
	tweet_texts = obj.get_tweets( list(df['tweet_id']) )
	df['tweet_text'] = tweet_texts
	df.to_csv('data/MovieTweets2.csv', index=False)


def add_tweet_tone(filepath):
	"""
	This function reads the csv produced from the previous function
	add_tweet_content() and gets the tweet text and use the IBM_ToneAnalyzer()
	class that we have just created to retireve the tweets' tone
	Args:
		filepath (string): the relative/absolute path of the csv file
	Returns:
		another csv file containing the tweet tones.
	"""
	df = pd.read_csv(filepath)
	# remove empty tweets
	df.dropna(how='any', inplace=True)
	obj = IBM_ToneAnalyzer()
	tweet_tones = obj.get_tweets_tone( list(df['tweet_text']) )
	# tweet_tones = [get_random_tone(random.randint(2, 5)) for _ in tqdm(list(df['tweet_text']))]
	df['tweet_tone'] = tweet_tones
	df.to_csv('data/MovieTweets.csv', index=False)






if __name__ == "__main__":
	# extract_info('data/test.dat', 'data/movies.dat')
	# add_tweet_content('data/MovieTweets1.csv')
	add_tweet_tone('data/MovieTweets2.csv')
