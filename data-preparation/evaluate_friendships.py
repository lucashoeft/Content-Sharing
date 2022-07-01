import pandas as pd

user_friendship_list = pd.read_csv('../data/processed/user_friendships.csv', sep=";", na_values="")
user_list = pd.read_csv('../data/processed/user_list.csv', sep=";", na_values="")


friendships = pd.DataFrame(columns=['source_screen_name',\
			'source_id',\
			'target_screen_name',\
			'target_id',\
			'source_follows_target',\
			'target_follows_source',\
			'tie_type'])

for index,contents in user_list.iterrows():
	source_screen_name = contents['twitter_handle']
	source_id = contents['twitter_id']
	for index, contents in user_list[index+1:].iterrows():
		target_screen_name = contents['twitter_handle']
		target_id = contents['twitter_id']
		print(source_screen_name, target_screen_name)


		# Check if source follows target
		source_follows_target_df = user_friendship_list[(user_friendship_list['source_screen_name'] == source_screen_name) & (user_friendship_list['target_screen_name'] == target_screen_name)]
		
		if source_follows_target_df.empty:
			source_follows_target = False
		else:
			source_follows_target = True

		# Check if target follows source
		target_follows_source_df = user_friendship_list[(user_friendship_list['source_screen_name'] == target_screen_name) & (user_friendship_list['target_screen_name'] == source_screen_name)]
		
		if target_follows_source_df.empty:
			target_follows_source = False
		else:
			target_follows_source = True

		# determine tie type
		if source_follows_target == True and target_follows_source == True:
			tie_type = "strong"
		elif source_follows_target == True or target_follows_source == True:
			tie_type = "weak"
		else:
			tie_type = "no tie"

		print(round(friendships.shape[0] / (user_friendship_list.shape[0]/2) * 100, 1), "%")

		friendships.loc[len(friendships.index)] = [source_screen_name, source_id, target_screen_name, target_id, source_follows_target, target_follows_source, tie_type]

print(friendships[['source_screen_name', 'target_screen_name', 'tie_type']])
	
friendships.to_csv('../data/processed/user_friendships_evaluation.csv', index=False, decimal=',', sep=";", float_format='%.f')