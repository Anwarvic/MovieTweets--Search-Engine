import os
from elasticsearch import Elasticsearch
from flask import Flask, render_template, request, redirect, url_for

from indexing import es_search


app = Flask(__name__)


@app.route('/')
def index():
	return render_template("index.html") #TODO: change temp.html to index.html


@app.route('/', methods=['POST'])
def my_form_post():
	text = request.form['search_query']
	return redirect(url_for('elastic_query', query_text=text))


@app.route('/query/<query_text>')
def elastic_query(query_text):
	hits = es_search(ES, query_text)
	query_out = [hit['_source'] for hit in hits]
	res = render_template('result.html', 
						  query_text=query_text,
						  toPass=query_out)
	return res



@app.route('/movie/<id_>')
def chart(id_):
	hits = es_search(ES, id_)
	out = hits[0]['_source']
	return render_template('dashboard.html',
							movie_name = out['movie_name'],
							tones=out['average_tones'],
							tweets = out['tweets'])



if __name__ == '__main__':
	ES = Elasticsearch([{'host':'localhost','port':9200}])
	app.run(debug = True)