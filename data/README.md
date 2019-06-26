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


