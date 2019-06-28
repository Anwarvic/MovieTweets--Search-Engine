# Data Preparation

Reading this file is optional and you can use the data without knowing how I got it. But if you want more information about how I got it, then reading this document will be suitable.

The data used in this repo is a data that contains reviews on IMDb movies on Twitter. The data is a csv file containing:

- `movie_id`: the Id of the movie on IMDb.
- `movie_name`: the name of the movie as shown on IMDb.
- `tweet_id`: the tweet id on Twitter.
- `tweet_text`: the tweet text.
- `tweet_tone`: the tone of the tweet.


 I have prepared this data using the following steps:

- Download this [MovieTwetings](https://github.com/sidooms/MovieTweetings/blob/master/recsyschallenge2014/recsys_challenge_2014_dataset.zip) data (65MB).
- After downloading it and uncompressing you will find a few files. We are interested in just one file `test.dat` which contains around 20,000 tweets
- Download [this data](https://github.com/sidooms/MovieTweetings/blob/master/latest/movies.dat) contains the movie names (2MB).
- Then, put the two file (`movies.dat` and `test.dat`) into a new directory called `data`.
- Run the `prepare_data.py` python script which would produce the `MovieTweets.csv` file.



## prepare_data.py

This script is used to obtain the data in three steps:

- Step1: obtaining what we want from `test.dat` and `movies.dat`.
- Step2: Getting tweets content.
- Step3: Getting Tones for tweets.
- Step4: Group data by movie



### Step1

The function responsible for doing this step is `extract_info()`. This function uses `test.dat` to extract `user_id`, `movie_id`, and `tweet_id`. And it uses `movies.dat` to extract `movie_name` for each single movie in our data. The output of this step is a csv file called `MovieTweets1.csv`.

 The resulting CSV from this step won't contain `tweet_text` or `tweet_tone` as both will be obtained in the following two steps. Also, it won't contain the whole 20,000 tweets in the `test.dat` file, just the first 10,000. Why is that? Apparently, Twitter puts a rate limit for retrieving data from its API. When you exceed this rate, you will a warning that says `Rate limit reached. Sleeping for: 758` which means that I had to slow down my retrieving rate to the extent that I have collected the 10,000 tweets in more than 3 hours.



### Step2

This step is responsible for getting only the `tweet_text` using Twitter API. The function responsible for that is `add_tweet_content()`  which uses the script `twitter.py` responsible for calling twitter API. The  resulting CSV will be called `MovieTweets2.csv` which will contain just one additional column (`tweet_text`).



### Step3

This step is responsible for getting the tone for our tweets using IBM Tone Analyzer. The function responsible for this job is `add_tweet_tone()` which uses `tone_analyzer.py`  to communicate with the IBM API. The  resulting CSV will be called `MovieTweets.csv` which will contain just one additional column (`tweet_tone`). The tweets in this data are so generic which have no tones. So, to make things interesting, I've generated random tones to each tweet in the data


### Step4

This step is simple. Here, we group the data from the last stem by `movie_id`. The resulting csv from this step is the one sent to ElasticSearch engine. This csv will containt these fileds `movie_id`, `movie_name`, `reviews_count`, `average_tones`, and `tweets`. It will look like this:


movie_id|movie_name|reviews_count|average_tones|tweets
|-------|---------|-------------|-------------|------|
|993846 |The Wolf of Wall Street (2013)|535|{'Anger': 0.2844859585329844, 'Fear': 0.2838749471226159, 'Joy': 0.27755553696029167, 'Sadness': 0.26465190869767846, 'Analytical': 0.2751570982991599, 'Confident': 0.2899761642095416, 'Tentative': 0.27979233958022803}|[{'tweet_id': 4.21051e+17, 'tweet_text': 'I rated The Wolf of Wall Street 1\/10  #IMDb http:\/\/t.co\/eJtRKX4VB5'}, ...]|