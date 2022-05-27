import pandas as pd

mdb_list = pd.read_csv('../data/processed/mdb_list/mdb_list.csv', sep=";")
twitter_usernames = pd.read_csv('../data/external/twitter_usernames.csv', sep=";")

# Merge mdb list with info about twitter usernames
mdb_twitter_list = pd.merge(mdb_list, twitter_usernames, on='bundestag_id')

print(mdb_list.shape)
print(twitter_usernames.shape)
print(mdb_twitter_list.shape)

mdb_twitter_list.to_csv('../data/processed/mdb_twitter_list/mdb_twitter_list.csv', index=False, sep=";")
