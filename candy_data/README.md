Датасет можно найти по ссылке: [https://www.scq.ubc.ca/so-much-candy-data-seriously/](https://www.scq.ubc.ca/so-much-candy-data-seriously/).

## О данных
Датасет состоит из ответов на опрос, опубликованный в октябре 2017 года. Опрос содержит следующие вопросы:
1. Q1: GOING OUT? (планирует ли респондент получать конфеты в честь праздника хэллоуин)
2. Q2: GENDER (пол респондента)
3. Q3: AGE (возвраст респондента)
4. Q4: COUNTRY (страна проживания респондента)
5. Q5: STATE, PROVINCE, COUNTY, ETC (штат,провинция, ...)
6. Q6: JOY OR DEPAIR? (для каждого вида конфеты респондент указывает свое отношение к нему - JOY (положительное), MEH (безразличное), или DESPAIR (отрицательное))
7. Q7: JOY OTHER (респондент может добавить не указанные выше виды конфет, которые доставляют им удовольствие)
8. Q8: DESPAIR OTHER (аналогично для негативно воспринимаемых конфет)
9. Q9: OTHER COMMENTS (дополнительные комментарии)

Далее идут вопросы, не связанные с темой сладостей:

11. Q10: DRESS (какого цвета платье на фотографии, популярная тема для спора в интернет сообществах)
12. Q11: DAY (какой день недели респондент предпочитает - Friday (пятницу) или Sunday (воскресенье))
13. Q12: MEDIA (респондент выбирает одну из четырех предложенных фотографий сайтов новостей)

## Обработка и очистка данных
Считываем данные из Excel таблицы и выводим названия всех столбцов и первый ненулевой элемент в каждом из них (для примера данных):
```
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
```
Далее обрабатываем возраст и пол:
```
df["Q2: GENDER"] = df["Q2: GENDER"].fillna("I'd rather not say") 
df["Q3: AGE"] = pd.to_numeric(df["Q3: AGE"], errors='coerce')
df = df[~df["Q3: AGE"].isna() & (df["Q3: AGE"] <= 130) & (df["Q3: AGE"] >= 0)]
```
Удаляем столбцы, в которых больше половины значений отсутствуют:
```
df_not_empty_cols = []
for col in df_columns:
    empty_cells_count = df[col].isnull().sum()
    total_cells_count = len(df[col])
    if total_cells_count == 0 or empty_cells_count / total_cells_count > 0.5:
        print(f'Column "{col}" has a high amount of empty cells: {empty_cells_count} out of {total_cells_count}')
    else:
        df_not_empty_cols.append(col)
df = df[df_not_empty_cols]
```
Удаляем столбцы последних трех вопросов:
```
df = df.drop(['Q10: DRESS', 'Q11: DAY', 'Q12: MEDIA [Science]', 'Click Coordinates (x, y)'], axis=1)
df_columns = df.columns
```
Проверяем, что все данные в одном столбце однотипны:
```
mixed_type_count = []
for col in df_columns:
    types_count = df[col].notnull().apply(type).value_counts()
    if len(types_count) > 1:
        mixed_type_count.append(col)
if len(mixed_type_count) > 0:
    print('Columns that have different types of data:', mixed_type_count)
else:
    print('OK. All columns have only 1 type of data in them')
```

## Анализ данных

Считаем процент приносящих радость конфет. Для упрощения восприятия считаем, что конфеты, которые вызывают радость хотя бы на 15% чаще, чем неудовольствие - "положительные", наоборот - "отрицательные", а остальные (то есть мало выдающиеся в том или ином направлении) - нейтральные.
```
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
```
Список видов конфет отсортирован по количеству положительных отзывов. Самой любимой конфетой оказалась "Any full-sized candy bar".

Проводим ту же оценку, но только для респондентов, планирующих участвовать в сборе конфет:
```
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
```
Визуализация датасета и наших вычислений:
```
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
```

## Дальнейшие действия

Показания для конфет можно и дальше разбить на подвыборки по возврасту, месту проживания и полу респондентов. 

Можно также оценить как изменились показания после ограничения на только планирующих собирать конфеты.
