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
