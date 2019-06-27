import pandas as pd
from tqdm import tqdm
from elasticsearch import Elasticsearch




def parse_row(row):
	output_dict = {}
	output_dict['movie_id'] = int(row['movie_id'])
	output_dict['movie_name'] = row['movie_name']
	output_dict['reviews_count'] = row['reviews_count']
	output_dict['average_tones'] = eval(row['average_tones'])
	output_dict['tweets'] = eval(row['tweets'])
	return output_dict



def index_data(data_filepath):
	es = Elasticsearch([{'host':'localhost','port':9200}])
	df = pd.read_csv(data_filepath)
	for idx, row in tqdm(df.iterrows(), desc="Indexing", total=len(df)):
		row = parse_row(row)
		es.index(index='megacorp', doc_type='movie_tweet', id=idx, body=row)
		# break




if __name__ == "__main__":
	index_data('data/MovieTweetsIndex.csv')
	