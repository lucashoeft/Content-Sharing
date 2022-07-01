import pandas as pd

retweet_list = pd.read_csv('../data/processed/quote_list.csv', sep=";", na_values="", lineterminator='\n')
user_friendship_list = pd.read_csv('../data/processed/user_friendships_evaluation.csv', sep=";", na_values="")
# print(retweet_list.dtypes)

weak = 0
strong = 0
notie = 0
notchecked = 0
sameperson = 0

for index, contents in retweet_list.drop_duplicates(subset=['tweet_id']).iterrows():
	# Original Author
	author_twitter_handle = contents['author_twitter_handle']
	# print(author_twitter_handle)

	# user_friendship_list = user_friendship_list[user_friendship_list['target_screen_name'] == author_twitter_handle]

	# get tweet id
	tweet_id = contents['tweet_id']

	# filter retweet_list based on tweet id
	retweets = retweet_list[retweet_list['tweet_id'] == tweet_id]

	# filter retweet_list that retweeter != tweeter
	#retweets = retweets[retweets['quoter_twitter_handle'] == retweets['author_twitter_handle']]

	retweets = retweets.reset_index(drop=True) # reset index

	# iterate over retweeters
	for index, contents in retweets.iterrows():
		print()
		print(contents['quoter_twitter_handle'], contents['quote_text'])
		retweeter_twitter_handle = contents['quoter_twitter_handle']
	
		# Get Relationship
		connection = user_friendship_list[(user_friendship_list['target_screen_name'].isin([author_twitter_handle, retweeter_twitter_handle])) & (user_friendship_list['source_screen_name'].isin([author_twitter_handle, retweeter_twitter_handle]))]
		if connection.shape[0] == 1:
			print("Friendship:", connection['tie_type'].iloc[0])

			if connection['tie_type'].iloc[0] == "strong":
				strong += 1
			elif connection['tie_type'].iloc[0] == "weak":
				weak += 1
			else:
				notie += 1

		else:
			if author_twitter_handle == retweeter_twitter_handle:
				sameperson += 1
			else:
				print("Friendship", author_twitter_handle, "&", retweeter_twitter_handle, 'not evaluated yet')
				notchecked += 1 

		# print(connection.shape)

print("weak:", weak)
print("strong:", strong)
print("notie:", notie)
print("notchecked", notchecked)
print("sameperson", sameperson)

	# Get Rate of weak-tie / strong-tie


# print(retweet_list.dtypes)