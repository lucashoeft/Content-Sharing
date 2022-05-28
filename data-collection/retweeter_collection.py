import pandas as pd
import os
import re

# read all files from the tweet_list folder in one dataframe
tweet_list = pd.DataFrame()
pattern = re.compile("tweet_list_*")
directory = "../data/processed/tweet_list/"

for filename in os.listdir(directory):
	if pattern.match(filename):
		print(filename)
		filepath = directory + filename
		user_tweet_list = pd.read_csv(filepath, sep=";", lineterminator='\n')
		tweet_list = pd.concat([tweet_list, user_tweet_list], axis=0)

# Create a dataframe with all retweets in the tweet_list dataframe
retweet_tweet_list = tweet_list[tweet_list['tweet_referenced_tweet_type'] == "retweeted"]

# Create a dataframe with all retweets that are related to tweets in the tweet_list dataframe
relevant_retweet_tweet_list = pd.merge(retweet_tweet_list, tweet_list, left_on='tweet_referenced_tweet_id', right_on='tweet_id')
relevant_retweet_tweet_list.drop(['twitter_id_x',\
	'tweet_conversation_id_x',\
	'tweet_in_reply_to_user_id_x',\
	'tweet_lang_x',\
	'tweet_possibly_sensitive_x',\
	'tweet_retweet_count_x',\
	'tweet_reply_count_x',\
	'tweet_like_count_x',\
	'tweet_quote_count_x',\
	'tweet_reply_settings_x',\
	'tweet_referenced_tweet_id_x',\
	'tweet_referenced_tweet_id_x',\
	'tweet_source_x',\
	'api_call_x',\
	'twitter_id_y',\
	'tweet_conversation_id_y',\
	'tweet_in_reply_to_user_id_y',\
	'tweet_lang_y',\
	'tweet_possibly_sensitive_y',\
	'tweet_retweet_count_y',\
	'tweet_reply_count_y',\
	'tweet_like_count_y',\
	'tweet_quote_count_y',\
	'tweet_reply_settings_y',\
	'tweet_source_y',\
	'tweet_referenced_tweet_id_y',\
	'tweet_referenced_tweet_type_y',\
	'api_call_y'], axis=1, inplace=True)
relevant_retweet_tweet_list.rename(columns={"tweet_author_id_x": "retweeter_twitter_id ",\
	"tweet_created_at_x": "retweet_created_at",\
	"twitter_handle_x": "retweeter_twitter_handle",\
	"tweet_id_x": "retweet_tweet_id",\
	"tweet_text_x": "retweet_text",\
	"twitter_handle_y": "author_twitter_handle",\
	"tweet_id_y": "tweet_id",\
	"tweet_text_y": "tweet_text",\
	"tweet_author_id_y": "author_twitter_id",\
	"tweet_created_at_y": "tweet_created_at"}, inplace=True)

# Create a dataframe with all quotes in the tweet_list dataframe
quote_tweet_list = tweet_list[tweet_list['tweet_referenced_tweet_type'] == "quoted"]

# Create a dataframe with all quotes that are related to tweets in the tweet_list dataframe
relevant_quote_tweet_list = pd.merge(quote_tweet_list, tweet_list, left_on='tweet_referenced_tweet_id', right_on='tweet_id')
relevant_quote_tweet_list.drop(['twitter_id_x',\
	'tweet_conversation_id_x',\
	'tweet_in_reply_to_user_id_x',\
	'tweet_lang_x',\
	'tweet_possibly_sensitive_x',\
	'tweet_retweet_count_x',\
	'tweet_reply_count_x',\
	'tweet_like_count_x',\
	'tweet_quote_count_x',\
	'tweet_reply_settings_x',\
	'tweet_referenced_tweet_id_x',\
	'tweet_referenced_tweet_id_x',\
	'tweet_source_x',\
	'api_call_x',\
	'twitter_id_y',\
	'tweet_conversation_id_y',\
	'tweet_in_reply_to_user_id_y',\
	'tweet_lang_y',\
	'tweet_possibly_sensitive_y',\
	'tweet_retweet_count_y',\
	'tweet_reply_count_y',\
	'tweet_like_count_y',\
	'tweet_quote_count_y',\
	'tweet_reply_settings_y',\
	'tweet_source_y',\
	'tweet_referenced_tweet_id_y',\
	'tweet_referenced_tweet_type_y',\
	'api_call_y'], axis=1, inplace=True)
relevant_quote_tweet_list.rename(columns={"tweet_author_id_x": "quoter_twitter_id ",\
	"tweet_created_at_x": "quote_created_at",\
	"twitter_handle_x": "quoter_twitter_handle",\
	"tweet_id_x": "quote_tweet_id",\
	"tweet_text_x": "quote_text",\
	"twitter_handle_y": "author_twitter_handle",\
	"tweet_id_y": "tweet_id",\
	"tweet_text_y": "tweet_text",\
	"tweet_author_id_y": "author_twitter_id",\
	"tweet_created_at_y": "tweet_created_at"}, inplace=True)

print("Number of Retweets:", relevant_retweet_tweet_list.shape[0])
print("Number of Quotes:", relevant_quote_tweet_list.shape[0])

# Store results
relevant_retweet_tweet_list.to_csv('../data/processed/retweet_list/retweet_list.csv', index=False, decimal=',', sep=";", float_format='%.0f')
relevant_quote_tweet_list.to_csv('../data/processed/retweet_list/quote_list.csv', index=False, decimal=',', sep=";", float_format='%.0f')