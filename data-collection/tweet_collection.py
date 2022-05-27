import config
import tweepy
from datetime import datetime
import numpy as np
import pandas as pd
import re
import os

client = tweepy.Client(bearer_token=config.bearer_token, wait_on_rate_limit=True)

user_list = pd.read_csv('../data/processed/user_list/user_list.csv', sep=";", na_values="", dtype={'twitter_id': str})

user_list = user_list.dropna(subset=['twitter_id']).head(10)

for index, contents in user_list.iterrows():

	twitter_id = np.int64(contents['twitter_id'])
	twitter_handle = contents['twitter_handle']#

	# Pattern for file with a twitter_id
	pattern = re.compile("tweet_list_" + str(twitter_id) + "_*")

	matching_file = False

	# Check flag to true if any file matches the criteria
	for filepath in os.listdir("../data/processed/tweet_list/"):
		if pattern.match(filepath):
			matching_file = True

	if not matching_file:
		print("### REQUEST", index, "###")
		print(twitter_id)
		print(twitter_handle)

		# available tweet_fields at https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
		# expansions https://docs.tweepy.org/en/stable/expansions_and_fields.html#expansions-parameter
		# tweets = client.get_users_tweets(id=twitter_id, tweet_fields=['attachments', 'author_id', 'context_annotations', 'conversation_id', 'created_at', 'entities', 'geo', 'lang', 'in_reply_to_user_id', 'possibly_sensitive', 'public_metrics', 'referenced_tweets', 'reply_settings', 'source'], max_results=5)

		tweet_list = pd.DataFrame(columns=['twitter_id',\
			'twitter_handle',\
			'tweet_id',\
			'tweet_text',\
			'tweet_author_id',\
			'tweet_conversation_id',\
			'tweet_created_at',\
			'tweet_in_reply_to_user_id',\
			'tweet_lang',\
			'tweet_possibly_sensitive',\
			'tweet_retweet_count',\
			'tweet_reply_count',\
			'tweet_like_count',\
			'tweet_quote_count',\
			'tweet_reply_settings',\
			'tweet_source',\
			'tweet_referenced_tweet_id',\
			'tweet_referenced_tweet_type',\
			"api_call"])
		
		# Check if tweets exist in the response
		for tweet in tweepy.Paginator(client.get_users_tweets, id=np.int64(twitter_id), tweet_fields=['attachments', 'author_id', 'context_annotations', 'conversation_id', 'created_at', 'entities', 'geo', 'lang', 'in_reply_to_user_id', 'possibly_sensitive', 'public_metrics', 'referenced_tweets', 'reply_settings', 'source'], max_results=100).flatten(limit=3200):
			tweet_id = tweet.id
			print(tweet_id)
			tweet_text = tweet.text
			tweet_author_id = tweet.author_id
			tweet_conversation_id = tweet.conversation_id
			tweet_created_at = tweet.created_at
			tweet_in_reply_to_user_id = tweet.in_reply_to_user_id
			tweet_lang = tweet.lang
			tweet_possibly_sensitive = tweet.possibly_sensitive

			tweet_retweet_count = tweet.public_metrics['retweet_count']
			tweet_reply_count = tweet.public_metrics['reply_count']
			tweet_like_count = tweet.public_metrics['like_count']
			tweet_quote_count = tweet.public_metrics['quote_count']
			tweet_reply_settings = tweet.reply_settings
			tweet_source = tweet.source

			# to find out if and which tweet was retweeted, quoted or replied to
			tweet_referenced_tweets = tweet.referenced_tweets # nested; not stored in dataframe
			tweet_referenced_tweet_id = ""
			tweet_referenced_tweet_type = ""
			if tweet_referenced_tweets is not None:
				tweet_referenced_tweet_id = tweet_referenced_tweets[0].id
				tweet_referenced_tweet_type = tweet_referenced_tweets[0].type

			# more meta data information which is currently not added to the data frame
			tweet_attachments = tweet.attachments # nested; not stored in dataframe
			tweet_context_annotations = tweet.context_annotations # nested; not stored in dataframe
			tweet_entities = tweet.entities # nested; not stored in dataframe
			tweet_geo = tweet.geo # nested; not stored in dataframe

			# Add Log from API Call
			api_call = datetime.now()
			
			tweet_list.loc[len(tweet_list.index)] = [twitter_id,\
				twitter_handle,\
				tweet_id,\
				tweet_text,\
				tweet_author_id,\
				tweet_conversation_id,\
				tweet_created_at,\
				tweet_in_reply_to_user_id,\
				tweet_lang,\
				tweet_possibly_sensitive,
				tweet_retweet_count,\
				tweet_reply_count,\
				tweet_like_count,\
				tweet_quote_count,\
				tweet_reply_settings,\
				tweet_source,\
				tweet_referenced_tweet_id,\
				tweet_referenced_tweet_type,\
				api_call]

		file_path = '../data/processed/tweet_list/tweet_list_' + str(twitter_id) + "_" + twitter_handle + '.csv'
		tweet_list.to_csv(file_path, index=False, decimal=',', sep=";", float_format='%.0f')