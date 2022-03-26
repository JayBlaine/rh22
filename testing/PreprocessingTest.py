import pandas as pd
import sys

synopsis_file = sys.argv[1]
rating_file = sys.argv[2]
sypnopsis_col_name = 'sypnopsis'
user_col_name = 'user_id'

synopsis_df = pd.read_csv(synopsis_file)
ratings_df = pd.read_csv(rating_file)

df = pd.DataFrame()
df['User ID'] = ratings_df[user_col_name]
print(df)