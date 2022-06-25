import config
import tweepy
from datetime import datetime
import numpy as np
import pandas as pd

client = tweepy.Client(bearer_token=config.bearer_token, wait_on_rate_limit=True)

# Authenticate to Twitter
auth = tweepy.OAuthHandler(config.api_key, config.api_secret_key)
auth.set_access_token(config.access_token, config.access_secret)
 
api = tweepy.API(auth, wait_on_rate_limit=True)
 
try:
    api.verify_credentials()
    print('Successful Authentication')
except:
    print('Failed authentication')

# Get user list
user_list = pd.read_csv('../data/processed/user_list/user_list.csv', sep=";", na_values="",  dtype={'twitter_id': str})
user_list = user_list.dropna(subset=['twitter_id'])

user_friendship_list = pd.read_csv('../data/processed/user_friendships/user_friendships.csv', sep=";", na_values="")

user_list = user_list.reset_index(drop=True) # reset index
for index, contents in user_list.iterrows():
	source_screen_name = user_list.iloc[index].twitter_handle
	source_id = user_list.iloc[index].twitter_id

	# get dataframe of all checked connections of source
	source_friendships = user_friendship_list[user_friendship_list['source_id'] == np.int64(source_id)]

	for index, contents in user_list[index:].iterrows(): 
		if index+1 < len(user_list):
			target_screen_name = user_list.iloc[index+1].twitter_handle
			target_id = user_list.iloc[index+1].twitter_id
				
			# check if target appears in source_friendships...
			target_frienship = source_friendships[source_friendships['target_id'] == np.int64(target_id)]
			
			if target_frienship.empty:
				try:
					friendship = api.get_friendship(source_screen_name=source_screen_name, target_screen_name=target_screen_name)
					now = datetime.now()
					print(now, source_screen_name, source_id, target_screen_name, target_id)
					
					if friendship[0].following:
						# source follows target
						user_friendship_list.loc[len(user_friendship_list.index)] = [source_screen_name, source_id, target_screen_name, target_id, True, now]
					else:
						# source does not follow target
						user_friendship_list.loc[len(user_friendship_list.index)] = [source_screen_name, source_id, target_screen_name, target_id, False, now]

					if friendship[0].followed_by:
						# target follows source
						user_friendship_list.loc[len(user_friendship_list.index)] = [target_screen_name, target_id, source_screen_name, source_id, True, now]
					else:
						# target does not follow source
						user_friendship_list.loc[len(user_friendship_list.index)] = [target_screen_name, target_id, source_screen_name, source_id, False, now]

					user_friendship_list.to_csv('../data/processed/user_friendships/user_friendships.csv', index=False, decimal=',', sep=";", float_format='%.f')
				except:
					print("ERROR")

	user_friendship_list.to_csv('../data/processed/user_friendships/user_friendships_' + str(source_screen_name) + '.csv' , index=False, decimal=',', sep=";", float_format='%.f')
"""

for index, contents in user_list.iterrows():
	source_screen_name = user_list.iloc[index].twitter_handle
	source_id = user_list.iloc[index].twitter_id
	print(source_id)

	n_friendships = user_friendship_list[user_friendship_list['source_id'] == np.int64(source_id)].shape[0]
	
	# check that not all possible users were checked for the user
	if n_friendships < user_list.shape[0]-1:
		print(source_screen_name, "made it")
		for index, contents in user_list[index:].iterrows(): 
			if index+1 < len(user_list):
				target_screen_name = user_list.iloc[index+1].twitter_handle
				target_id = user_list.iloc[index+1].twitter_id
				print(target_screen_name)
				
				if user_friendship_list.empty:
					api_call += 1
					now = datetime.now()
					print("b", now, source_screen_name, source_id, target_screen_name, target_id)
					
					try:
						friendship = api.get_friendship(source_screen_name=source_screen_name, target_screen_name=target_screen_name)
					except:
						print("ERROR")

					print("a", now, source_screen_name, source_id, target_screen_name, target_id)
					
					try:
						print(friendship[0].following)
					except NotFound:
						print(source_screen_name, "or", target_screen_name, "not found")

					if friendship[0].following:
						# source follows target
						user_friendship_list.loc[len(user_friendship_list.index)] = [source_screen_name, source_id, target_screen_name, target_id, True, now]
					else:
						# source does not follow target
						user_friendship_list.loc[len(user_friendship_list.index)] = [source_screen_name, source_id, target_screen_name, target_id, False, now]

					if friendship[0].followed_by:
						# target follows source
						user_friendship_list.loc[len(user_friendship_list.index)] = [target_screen_name, target_id, source_screen_name, source_id, True, now]
					else:
						# target does not follow source
						user_friendship_list.loc[len(user_friendship_list.index)] = [target_screen_name, target_id, source_screen_name, source_id, False, now]
				else:
					# check if already exists in table
					check_friendship = user_friendship_list[(user_friendship_list['source_id'] == np.int64(source_id)) & (user_friendship_list['target_id'] == np.int64(target_id))]
					
					if check_friendship.empty:
						now = datetime.now()
						print("b", now, source_screen_name, source_id, target_screen_name, target_id)
						
						try:
							friendship = api.get_friendship(source_screen_name=source_screen_name, target_screen_name=target_screen_name)
						except:
							print("ERROR")

						print("a", now, source_screen_name, source_id, target_screen_name, target_id)
						
						try:
							print(friendship[0].following)
						except NotFound:
							print(source_screen_name, "or", target_screen_name, "not found")


						if friendship[0].following:
							# source follows target
							user_friendship_list.loc[len(user_friendship_list.index)] = [source_screen_name, source_id, target_screen_name, target_id, True, now]
						else:
							# source does not follow target
							user_friendship_list.loc[len(user_friendship_list.index)] = [source_screen_name, source_id, target_screen_name, target_id, False, now]

						if friendship[0].followed_by:
							# target follows source
							user_friendship_list.loc[len(user_friendship_list.index)] = [target_screen_name, target_id, source_screen_name, source_id, True, now]
						else:
							# target does not follow source
							user_friendship_list.loc[len(user_friendship_list.index)] = [target_screen_name, target_id, source_screen_name, source_id, False, now]
					else:
						continue
						# print("Already checked")

				user_friendship_list.to_csv('../data/processed/user_friendships/user_friendships.csv', index=False, decimal=',', sep=";", float_format='%.f')

				"""