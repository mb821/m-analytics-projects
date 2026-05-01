import pandas as pd
import numpy as np

df = pd.read_excel("candyhierarchy2017.xlsx", nrows=100)
print('Dataset columns:')
df_columns = list(df.columns)
for c in range(len(df_columns)):
    example_idx = df[df_columns[c]].first_valid_index()
    example = np.nan
    if example_idx:
        example = df[df_columns[c]].loc[example_idx]
    print(f'{c + 1}. "{df_columns[c]}" (e.g. {example})')
