import pandas as pd

user_friendship_list = pd.read_csv('../data/processed/user_friendships/user_friendships.csv', sep=";", na_values="")

friendships = pd.DataFrame(columns=['source_screen_name',\
			'source_id',\
			'target_screen_name',\
			'target_id',\
			'source_follows_target',\
			'target_follows_source',\
			'tie_type'])


for index, contents in user_friendship_list.iterrows():
	source_screen_name = contents['source_screen_name']
	source_id = contents['source_id']
	target_screen_name = contents['target_screen_name']
	target_id = contents['target_id']

	currentPair = contents # current row
	
	if index+1 < user_friendship_list.shape[0]:
		nextPair = user_friendship_list.iloc[index+1] # next row

		# check if this row and the next row are about the same two people
		if currentPair['source_screen_name'] == nextPair['target_screen_name'] and currentPair['target_screen_name'] == nextPair['source_screen_name']:
			source_follows_target = currentPair['following']
			target_follows_source = nextPair['following']

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

friendships.to_csv('../data/processed/user_friendships/user_friendships_evaluation.csv', index=False, decimal=',', sep=";", float_format='%.f')