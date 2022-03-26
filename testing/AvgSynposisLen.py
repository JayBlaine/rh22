from pydoc import synopsis
from statistics import mean
import sys
import pandas as pd

synopsis_file = sys.argv[1]
sypnopsis_col_name = 'sypnopsis'
df = pd.read_csv(synopsis_file)
df[sypnopsis_col_name] = df[sypnopsis_col_name].astype(str)
# print(df.loc[df[sypnopsis_col_name].str.isnumeric()])
print('Avg Synposis Length %.2f:' % df[sypnopsis_col_name].apply(len).mean())
print('Min Synposis Length %.2f:' % df[sypnopsis_col_name].apply(len).min())
print('Max Synposis Length %.2f:' % df[sypnopsis_col_name].apply(len).max())
