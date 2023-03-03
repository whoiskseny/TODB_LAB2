#!/usr/bin/env python
# coding: utf-8

# # Pandas

# ## Лабораторная работа №2

# ### Базовые операции с `DataFrame`

# 1.1 В файлах `recipes_sample.csv` и `reviews_sample.csv` находится информация об рецептах блюд и отзывах на эти рецепты соответственно. Загрузите данные из файлов в виде `pd.DataFrame` с названиями `recipes` и `reviews`. Обратите внимание на корректное считывание столбца с индексами в таблице `reviews` (безымянный столбец).

# 2.1 Преобразуйте столбец `submitted` из таблицы `recipes` в формат времени. Модифицируйте решение задачи 1.1 так, чтобы считать столбец сразу в нужном формате.

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


recipes = pd.read_csv('recipes_sample.csv', parse_dates=['submitted'])
reviews = pd.read_csv('reviews_sample.csv', index_col=[0])
recipes[:3]


# 1.2 Для каждой из таблиц выведите основные параметры:
# * количество точек данных (строк);
# * количество столбцов;
# * тип данных каждого столбца.

# In[4]:


#for recipes
print('Количество строк для первой таблицы =',len(recipes.axes[0]),
      '\nКоличество столбцов для первой таблицы =', len(recipes.axes[1]))
for i in range(0,len(recipes.axes[1])):
    print('Тип данных для',i+1, 'столбца:',type(recipes.iloc[0, i]))


# In[5]:


#for reviews
print('Количество строк для второй таблицы =',len(reviews.axes[0]),
      '\nКоличество столбцов для второй таблицы =', len(reviews.axes[1]))
for i in range(0,len(reviews.axes[1])):
    print('Тип данных для',i+1, 'столбца:',type(reviews.iloc[0,i]))


# 1.3 Исследуйте, в каких столбцах таблиц содержатся пропуски. Посчитайте долю строк, содержащих пропуски, в отношении к общему количеству строк.

# In[6]:


#for recipes
null_rows_total1 = recipes.shape[0] - recipes.dropna().shape[0]      #кол-во строк с пропусками
print('Количество пропусков в каждом столбце первой таблицы:\n', recipes.isna().sum())
print('Доля строк, содержащих пропуски: ', (null_rows_total1/len(recipes.axes[0]))*100,'%',sep='' )


# In[7]:


#for reviews
null_rows_total2 = reviews.shape[0] - reviews.dropna().shape[0]
print('Количество пропусков в каждом столбце второй таблицы:\n', reviews.isna().sum())
print('Доля строк, содержащих пропуски: ', (null_rows_total2/len(reviews.axes[0]))*100,'%',sep='' )


# 1.4 Рассчитайте среднее значение для каждого из числовых столбцов (где это имеет смысл).

# In[8]:


#for recipes
print('Среднее значение для столбца minutes: ', recipes['minutes'].mean(), 
      '\nСреднее значение для столбца n_steps: ', recipes['n_steps'].mean(), 
      '\nСреднее значение для столбца n_ingredients: ', recipes['n_ingredients'].mean())


# In[9]:


#for reviews
print('Среднее значение для столбца rating: ', reviews['rating'].mean())


# 1.5 Создайте серию из 10 случайных названий рецептов.

# In[10]:


ten_recipes = pd.Series(recipes['name'].sample(n = 10))
ten_recipes


# 1.6 Измените индекс в таблице `reviews`, пронумеровав строки, начиная с нуля.

# In[11]:


reviews.reset_index()


# 1.7 Выведите информацию о рецептах, время выполнения которых не больше 20 минут и кол-во ингредиентов в которых не больше 5.

# In[12]:


recipes[(recipes.minutes < 21) & (recipes.n_ingredients < 6)]


# ### Работа с датами в `pandas`

# 2.2 Выведите информацию о рецептах, добавленных в датасет не позже 2010 года.

# In[20]:


recipes[recipes['submitted']>='2010-01-01']


# ### Работа со строковыми данными в `pandas`

# 3.1  Добавьте в таблицу `recipes` столбец `description_length`, в котором хранится длина описания рецепта из столбца `description`.

# In[31]:


recipes['description_length']  = recipes['description'].str.len()


# 3.2 Измените название каждого рецепта в таблице `recipes` таким образом, чтобы каждое слово в названии начиналось с прописной буквы.

# In[40]:


recipes['name'] = recipes['name'].str.capitalize()


# 3.3 Добавьте в таблицу `recipes` столбец `name_word_count`, в котором хранится количество слов из названии рецепта (считайте, что слова в названии разделяются только пробелами). Обратите внимание, что между словами может располагаться несколько пробелов подряд.

# In[44]:


recipes['name_word_count'] = [len(x.split()) for x in recipes['name'].tolist()]


# ### Группировки таблиц `pd.DataFrame`

# 4.1 Посчитайте количество рецептов, представленных каждым из участников (`contributor_id`). Какой участник добавил максимальное кол-во рецептов?

# In[73]:


c = recipes.groupby("contributor_id").size()
print('Количество рецептов, представленных каждым из участников', c, 
      '\nУчастник, добавивший наибольшее кол-во рецептов: ', 
      c[c == c.max()].index[0])


# 4.2 Посчитайте средний рейтинг к каждому из рецептов. Для скольких рецептов отсутствуют отзывы? Обратите внимание, что отзыв с нулевым рейтингом или не заполненным текстовым описанием не считается отсутствующим.

# In[149]:


print('Кол-во рецептов, для которых отсутствуют отзывы', 
      len(recipes.groupby('name').size()) - len(reviews.groupby('recipe_id').size()))
reviews.groupby('recipe_id').mean('rating').drop('user_id', axis=1)


# 4.3 Посчитайте количество рецептов с разбивкой по годам создания.

# In[142]:


recipes.groupby(recipes.submitted.dt.year).size()


# ### Объединение таблиц `pd.DataFrame`

# 5.1 При помощи объединения таблиц, создайте `DataFrame`, состоящий из четырех столбцов: `id`, `name`, `user_id`, `rating`. Рецепты, на которые не оставлен ни один отзыв, должны отсутствовать в полученной таблице. Подтвердите правильность работы вашего кода, выбрав рецепт, не имеющий отзывов, и попытавшись найти строку, соответствующую этому рецепту, в полученном `DataFrame`.

# 5.2 При помощи объединения таблиц и группировок, создайте `DataFrame`, состоящий из трех столбцов: `recipe_id`, `name`, `review_count`, где столбец `review_count` содержит кол-во отзывов, оставленных на рецепт `recipe_id`. У рецептов, на которые не оставлен ни один отзыв, в столбце `review_count` должен быть указан 0. Подтвердите правильность работы вашего кода, выбрав рецепт, не имеющий отзывов, и найдя строку, соответствующую этому рецепту, в полученном `DataFrame`.

# 5.3. Выясните, рецепты, добавленные в каком году, имеют наименьший средний рейтинг?

# ### Сохранение таблиц `pd.DataFrame`

# 6.1 Отсортируйте таблицу в порядке убывания величины столбца `name_word_count` и сохраните результаты выполнения заданий 3.1-3.3 в csv файл. 

# 6.2 Воспользовавшись `pd.ExcelWriter`, cохраните результаты 5.1 и 5.2 в файл: на лист с названием `Рецепты с оценками` сохраните результаты выполнения 5.1; на лист с названием `Количество отзывов по рецептам` сохраните результаты выполнения 5.2.

# In[ ]:





# In[ ]:





# #### [версия 2]
# * Уточнены формулировки задач 1.1, 3.3, 4.2, 5.1, 5.2, 5.3

# In[ ]:




