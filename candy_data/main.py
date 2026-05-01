import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel("candyhierarchy2017.xlsx")
print('Dataset read. Size:', df.shape)

print('Dataset columns:')
print('--------------------------------------------------')
df_columns = list(df.columns)
for c in range(len(df_columns)):
    example_idx = df[df_columns[c]].first_valid_index()
    example = np.nan
    if example_idx:
        example = df[df_columns[c]].loc[example_idx]
    print(f'{c + 1}. "{df_columns[c]}" (e.g. {example})')
print('--------------------------------------------------')

print(f'Column "Q2: GENDER" has {df["Q2: GENDER"].isna().sum()} empty cells.')
df["Q2: GENDER"] = df["Q2: GENDER"].fillna("I'd rather not say") 

df["Q3: AGE"] = pd.to_numeric(df["Q3: AGE"], errors='coerce')
print(f'Column "Q3: AGE" has {df[(df["Q3: AGE"].isna()) | (df["Q3: AGE"] > 130) | (df["Q3: AGE"] < 0)].shape[0]} cells that are incorrect type, empty, or not believable human age (between 0 and 130)')
df = df[~df["Q3: AGE"].isna() & (df["Q3: AGE"] <= 130) & (df["Q3: AGE"] >= 0)]

df_not_empty_cols = []
for col in df_columns:
    empty_cells_count = df[col].isnull().sum()
    total_cells_count = len(df[col])
    if total_cells_count == 0 or empty_cells_count / total_cells_count > 0.5:
        print(f'Column "{col}" has a high amount of empty cells: {empty_cells_count} out of {total_cells_count}')
    else:
        df_not_empty_cols.append(col)
df = df[df_not_empty_cols]
print('Empty columns deleted. New dataframe size:', df.shape)

# I was curious about this part but it's irrelevant to the analysis ++++
print('Checking out the coordinates in column "Click Coordinates (x, y)"')
print('(Close the graph window to continue)')
coors = df[~df["Click Coordinates (x, y)"].isna()]["Click Coordinates (x, y)"]
x_coords = []
y_coords = []
for c in coors:
    if isinstance(c, tuple):
        x, y = c 
        x_coords.append(x)
        y_coords.append(y)
    elif isinstance(c, str):
        c1 = c.strip('()').split(',')
        if len(c1) == 2:
            x, y = c1
            x_coords.append(x)
            y_coords.append(y)
plt.scatter(x_coords, y_coords)
plt.axis('off')
plt.title('Click Coordinates (x, y)')
plt.show()
print('As you can see, the clicks are mostly in the bottom left corner')
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Deleting the last 3 questions due to them being unrelated to candy
df = df.drop(['Q10: DRESS', 'Q11: DAY', 'Q12: MEDIA [Science]', 'Click Coordinates (x, y)'], axis=1)
print('Deleted last 3 questions. Number of remaining columns:', df.shape[1])
df_columns = df.columns

print('Checking data types')
mixed_type_count = []
for col in df_columns:
    types_count = df[col].notnull().apply(type).value_counts()
    if len(types_count) > 1:
        mixed_type_count.append(col)
if len(mixed_type_count) > 0:
    print('Columns that have different types of data:', mixed_type_count)
else:
    print('OK. All columns have only 1 type of data in them')

print('================================================')
print('Data statistics:')
candy_only = df.filter(like='Q6')
print(f'Sorted percentage of joy and despair of each candy (total {candy_only.shape[1]} candy types) --------------------')
total_rows = candy_only.shape[0]
positive_candy = 0
negative_candy = 0
positive_count = candy_only.eq('JOY').sum()
candy_only = candy_only[positive_count.sort_values(ascending=False).index]
joys_all = []
despairs_all = []
for c in candy_only.columns:
    joy = (candy_only[c] == 'JOY').sum()
    despair = (candy_only[c] == 'DESPAIR').sum()
    joys_all.append(joy)
    despairs_all.append(despair)
    indicator = 'o'
    if (joy - despair) / total_rows > 0.15: # if joy > despair by 15% or more => positive
        indicator = '+'
        positive_candy += 1
    elif (joy - despair) / total_rows < -0.15: # if joy < despair by 15% or more => negative
        indicator = '-'
        negative_candy += 1
    print(f'{indicator} {c.strip("Q6 | ")}: JOY = {round(100*joy/total_rows)}%, DESPAIR = {round(100*despair/total_rows)}%')
print('------------------------------')
print(f'Total of {positive_candy} candy types were happily received, {negative_candy} were unhappily received, and {candy_only.shape[1] - positive_candy - negative_candy} were neither')

candy_only_going = df[df["Q1: GOING OUT?"] == 'Yes'].filter(like='Q6')
total_rows = candy_only_going.shape[0]
positive_candy_going = 0
negative_candy_going = 0
positive_count_going = candy_only_going.eq('JOY').sum()
candy_only_going = candy_only_going[positive_count_going.sort_values(ascending=False).index]
for c in candy_only_going.columns:
    joy = (candy_only_going[c] == 'JOY').sum()
    despair = (candy_only_going[c] == 'DESPAIR').sum()
    if (joy - despair) / total_rows > 0.15: # if joy > despair by 15% or more => positive
        positive_candy_going += 1
    elif (joy - despair) / total_rows < -0.15: # if joy < despair by 15% or more => negative
        negative_candy_going += 1
print(f'For people planning to go trick-or-treating total of {positive_candy_going} candy types were happily received, {negative_candy_going} were unhappily received, and {candy_only_going.shape[1] - positive_candy_going - negative_candy_going} were neither')


fig, axes = plt.subplots(2, 2)
axes[0, 0].set_title('Total candy reception')
axes[0, 0].pie([positive_candy, negative_candy, candy_only.shape[1] - positive_candy - negative_candy], labels=['JOY', 'DESPAIR', 'NEUTRAL'])

axes[1, 0].set_title('Trick-or-treaters candy reception')
axes[1, 0].pie([positive_candy_going, negative_candy_going, candy_only_going.shape[1] - positive_candy_going - negative_candy_going], labels=['JOY', 'DESPAIR', 'NEUTRAL'])

ages_counts = df["Q3: AGE"].value_counts()
axes[0, 1].bar(ages_counts.index.tolist(), ages_counts.values.tolist())
axes[0, 1].set_xlabel('Years')
axes[0, 1].set_ylabel('People')
axes[0, 1].set_title('Age')

axes[1, 1].bar(candy_only.columns, despairs_all, label='Despair', color='red')
axes[1, 1].bar(candy_only.columns, joys_all, bottom=despairs_all, label='Joy', color='green')
axes[1, 1].axis('off')
axes[1, 1].set_title('Reception for candy types')

plt.tight_layout()
plt.show()
