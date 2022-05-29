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

	other_friendship = friendships[(friendships['source_screen_name'] == contents['target_screen_name']) & (friendships['target_screen_name'] == contents['source_screen_name'])]

	# Check if the friendship was already checked the other way around
	if other_friendship.empty:
		source_screen_name = contents['source_screen_name']
		source_id = contents['source_id']

		target_screen_name = contents['target_screen_name']
		target_id = contents['target_id']

		source_follows_target = contents['following']
		
		target_source = user_friendship_list[(user_friendship_list['source_screen_name'] == contents['target_screen_name']) & (user_friendship_list['target_screen_name'] == contents['source_screen_name'])].iloc[0]
		target_follows_source = target_source['following']

		if source_follows_target == True & target_follows_source == True:
			tie_type = "strong"
		elif source_follows_target == False & target_follows_source == False:
			tie_type = "no tie"
		else:
			tie_type = "weak"

		friendships.loc[len(friendships.index)] = [source_screen_name, source_id, target_screen_name, target_id, source_follows_target, target_follows_source, tie_type]

print(friendships)

friendships.to_csv('../data/processed/user_friendships/user_friendships_evaluation.csv', index=False, decimal=',', sep=";", float_format='%.f')