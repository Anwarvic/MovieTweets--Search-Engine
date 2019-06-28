import pandas as pd
from tqdm import tqdm
from elasticsearch import Elasticsearch




def parse_row(row):
	"""
	This simple function to handle the data within dataframe row. By handling,
	I mean to parse numbers and objects before indexing them.
	NOTE: Here, we have converted 'movie_id' to int and 'average_tones' to dict
	and	'tweets' to a list
	"""
	output_dict = {}
	output_dict['movie_id'] = int(row['movie_id'])
	output_dict['movie_name'] = row['movie_name']
	output_dict['reviews_count'] = row['reviews_count']
	output_dict['average_tones'] = eval(row['average_tones'])
	output_dict['tweets'] = eval(row['tweets'])
	return output_dict



def index_data(data_filepath):
	"""
	This function does the ElasticSearch indexing. Indexing is a term which
	means entering the data in a certain structure into ElasticSearch engine.
	Args:
		data_filepath (string): the relative/absolute path of the CSV file.
	Returns:
		None
	"""
	es = Elasticsearch([{'host':'localhost','port':9200}])
	df = pd.read_csv(data_filepath)
	for idx, row in tqdm(df.iterrows(), desc="Indexing", total=len(df)):
		row = parse_row(row)
		es.index(index='megacorp', doc_type='movie_tweet', id=idx, body=row)
		# break


def es_search(es_object, user_query):
	"""
	This function is for searching data inside ElasticSearch. There are two
	paths w.r.t the search:
	 - if the query is a number, then we search inside 'movie_id', 'tweet_id'
	 	and 'reviews_count'
	 - if the query is a text, then we search in 'movie_name' and 'tweet_text'.
	Args:
		es_object (ElasticSearch): the Elastic Search object that connects the
			app to the engine.
		user_query (text/int): the query that the user wants to search for.
	Returns:
		a list of results, each result is a dictionary
	"""
	if user_query.isdigit():
		res= es_object.search(index='megacorp',body={
				'query':{
					'multi_match':{
						'query': user_query,
						'type': 'cross_fields',
						'fields':['movie_id', 'tweets.tweet_id', 'reviews_count']
					}
				}
			})
	else:
		res= es_object.search(index='megacorp',body={
				'query':{
					'multi_match':{
						'query': user_query,
						'type': 'cross_fields',
						'fields':['movie_name', 'tweets.tweet_text']
					}
				}
			})
	hits = res['hits']['hits']
	return hits




if __name__ == "__main__":
	# index_data('data/MovieTweetsIndex.csv')
	es = Elasticsearch([{'host':'localhost','port':9200}])
	for hit in es_search(es, '1130884'):
		print(hit['_score'])
		print(hit['_source']['movie_name'], hit['_source']['reviews_count'])