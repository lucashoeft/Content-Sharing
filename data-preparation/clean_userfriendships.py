from datetime import datetime
import numpy as np
import pandas as pd

user_friendship_list = pd.read_csv('../data/processed/user_friendships/user_friendships.csv', sep=";", na_values="")
user_friendship_list = pd.read_csv('../data/processed/user_friendships/user_friendships_secondary.csv', sep=";", na_values="")

user_list = pd.read_csv('../data/processed/user_list/user_list.csv', sep=";", na_values="", dtype={'twitter_id': str})

user_list = user_list[user_list['twitter_id'].notnull()]

print(user_list.shape)

print(user_friendship_list.shape)

print(user_friendship_list[~user_friendship_list['source_screen_name'].isin(user_list['twitter_handle'])])

print(user_friendship_list.shape)

print(user_friendship_list[~user_friendship_list['target_screen_name'].isin(user_list['twitter_handle'])][['target_screen_name', 'source_screen_name']])

print(user_friendship_list.shape)

