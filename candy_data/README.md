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

## Программная обработка
```
import pandas as pd
import numpy as np

df = pd.read_excel("candyhierarchy2017.xlsx")
print('Dataset columns:')
df_columns = list(df.columns)
for c in range(len(df_columns)):
    example_idx = df[df_columns[c]].first_valid_index()
    example = np.nan
    if example_idx:
        example = df[df_columns[c]].loc[example_idx]
    print(f'{c + 1}. "{df_columns[c]}" (e.g. {example})')
```
Считываем данные из Excel таблицы и выводим названия всех столбцов и первый ненулевой элемент в каждом из них (для примера данных).

## Выводы

