import config
import tweepy
from datetime import datetime
import numpy as np
import pandas as pd
import os.path

client = tweepy.Client(bearer_token=config.bearer_token, wait_on_rate_limit=True)

mdb_twitter_list = pd.read_csv('../data/processed/mdb_twitter_list/mdb_twitter_list.csv', sep=";", na_values="NA")

if not os.path.exists('../data/processed/user_list/user_list.csv'):
	# Fill user list with mdb_accounts if user_list does not exist
	mdb_twitter_list.to_csv('../data/processed/user_list/user_list.csv', index=False, decimal=',', sep=";", float_format='%.0f')

user_list = pd.read_csv('../data/processed/user_list/user_list.csv', sep=";", na_values="")

# For testing purposes and to reduce API calls, drop all entries without a twitter_handle which is used for the API calls
user_list = user_list.dropna(subset=['twitter_handle'])

for index, contents in user_list.iterrows():

	# first check if api_call column exists
	if 'api_call' in user_list.columns:

		api_call_value = contents['api_call']
		if isinstance(api_call_value, float):
			# do api call because float means value is  NA
			response = client.get_user(username=contents['twitter_handle'], user_fields=['created_at', 'description', 'location', 'protected', 'public_metrics', 'verified'])
			print(contents['twitter_handle'])

			# Check if user account was deleted in the meantime (= no account was found)
			if response.data is not None:
				# Append default Response Values
				user_list.at[index, 'twitter_id'] = response.data.id
				user_list.at[index, 'twitter_name'] = response.data.name

				# Append Responses of user_fields
				user_list.at[index, 'created_at'] = response.data.created_at
				user_list.at[index, 'description'] = response.data.description
				user_list.at[index, 'location'] = response.data.location
				user_list.at[index, 'protected'] = response.data.protected
				user_list.at[index, 'followers_count'] = response.data.public_metrics['followers_count']
				user_list.at[index, 'following_count'] = response.data.public_metrics['following_count']
				user_list.at[index, 'tweet_count'] = response.data.public_metrics['tweet_count']
				user_list.at[index, 'listed_count'] = response.data.public_metrics['listed_count']
				user_list.at[index, 'verified'] = response.data.verified

			# Log API Call Time
			now = datetime.now()
			user_list.at[index, 'api_call'] = now
		else:
			# variable is of type str (date is stored in column api_call so entry exists)
			continue

	else:
		# Make first API Call that also creates the api_call column
		response = client.get_user(username=contents['twitter_handle'], user_fields=['created_at', 'description', 'location', 'protected', 'public_metrics', 'verified'])
		print(contents['twitter_handle'])

		# Check if user account was deleted in the meantime (= no account was found)
		if response.data is not None:
			# Append default Response Values
			user_list.at[index, 'twitter_id'] = response.data.id
			user_list.at[index, 'twitter_name'] = response.data.name

			# Append Responses of user_fields
			user_list.at[index, 'created_at'] = response.data.created_at
			user_list.at[index, 'description'] = response.data.description
			user_list.at[index, 'location'] = response.data.location
			user_list.at[index, 'protected'] = response.data.protected
			user_list.at[index, 'followers_count'] = response.data.public_metrics['followers_count']
			user_list.at[index, 'following_count'] = response.data.public_metrics['following_count']
			user_list.at[index, 'tweet_count'] = response.data.public_metrics['tweet_count']
			user_list.at[index, 'listed_count'] = response.data.public_metrics['listed_count']
			user_list.at[index, 'verified'] = response.data.verified

		# Log API Call Time
		now = datetime.now()
		user_list.at[index, 'api_call'] = now
	
	# Store enriched data frame as new csv-file
	user_list.to_csv('../data/processed/user_list/user_list.csv', index=False, decimal=',', sep=";", float_format='%.0f')