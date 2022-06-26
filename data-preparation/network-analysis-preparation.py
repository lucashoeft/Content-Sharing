import pandas as pd

# Make Table for Nodes
# Make Table for Edges (Only True Matches)

user_list = pd.read_csv('../data/processed/user_list/user_list.csv', sep=";", na_values="", dtype={'twitter_id': str})

user_list = user_list[user_list['twitter_id'].notnull()]
user_list = user_list[['twitter_handle', 'fraktion']]
user_list.rename(columns = {'twitter_handle': 'Id', 'fraktion': 'Fraktion'}, inplace=True)


user_list.to_csv('../data/processed/network_analysis/nodes.csv', index=False, decimal=',', sep=";", float_format='%.0f')

user_friendship_list = pd.read_csv('../data/processed/user_friendships/user_friendships.csv', sep=";", na_values="")
user_friendship_list = user_friendship_list[user_friendship_list['following'] == True]
user_friendship_list = user_friendship_list[['source_screen_name', 'target_screen_name']]
user_friendship_list.rename(columns = {'source_screen_name': 'Source', 'target_screen_name': 'Target'}, inplace=True)

user_friendship_list.to_csv('../data/processed/network_analysis/edges.csv', index=False, decimal=',', sep=";", float_format='%.f')