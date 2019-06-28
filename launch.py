import os
from flask import Flask, render_template



app = Flask(__name__)


@app.route('/')
def index():
	return render_template("index.html")



if __name__ == '__main__':
	ES = Elasticsearch([{'host':'localhost','port':9200}])
	app.run(debug = True)