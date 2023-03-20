import re
import pandas as pd
# import numpy as np
from constants import *


class Preprocessor:
    def __init__(self, datasetPath: str):
        self.raw_df = pd.read_excel(datasetPath)
        self.raw_df['index'] = self.raw_df.index
        # self.raw_df.set_index('index', inplace=True)

        self.processed_df = None

    def __convertTimeToMinutes(self, time: str):
        x = re.search("\d+", time)

        if not x:
            return 0
        return int(x.group())

    def __convertCategoric(self, x: str):
        italian = x.lower()
        result = TRANSLATION_DICT[italian]
        return result

    def process(self):
        # Selecting only the relevant features
        relevant_features = ['index', 'cost', 'category', 'totalTime',
                             'difficulty', 'bestRating', 'ratingCount', 'ratingValue']
        df = self.raw_df[relevant_features]

        # Dropping nullvalues for columns
        # df = df[df['difficulty'].notnull()]
        # df = df[df['ratingValue'].notnull()]
        # df = df[df['ratingCount'].notnull()]
        # df = df[df['bestRating'].notnull()]
        # df = df[df['cost'].notnull()]
        df["ratingCount"].fillna(0.1, inplace=True)
        df["ratingValue"].fillna(0.1, inplace=True)
        df["totalTime"].fillna("nan", inplace=True)
        df["difficulty"].fillna("media", inplace=True)
        df["cost"].fillna("medio", inplace=True)

        # Applying language conversion to categoric features, as well as converting time to numeric
        df['totalMinutes'] = df['totalTime'].apply(self.__convertTimeToMinutes)
        df['category'] = df['category'].apply(self.__convertCategoric)
        df['cost'] = df['cost'].apply(self.__convertCategoric)
        df['difficulty'] = df['difficulty'].apply(self.__convertCategoric)

        # Dropping the totalTime column, we don't need it as we created new column after conversion
        df = df.drop('totalTime', axis=1)

        self.processed_df = df

    def list_all(self):
        recipes = self.processed_df.copy()
        recipes = recipes[['index']]

        # Makes sure to return only recipes that went through processing (excluding nullvalues etc)
        recipes_indexes = recipes.index.to_list()
        raw_recipes = self.raw_df.iloc[recipes_indexes]

        recipes['label'] = raw_recipes['title']
        recipes['id'] = recipes['index']
        recipes = recipes.drop('index', axis=1)

        recipes = recipes.drop_duplicates(
            subset="label", keep=False, inplace=False)
        return recipes

    def build_chart(self, maxPrice: int, maxMinutes: int, maxDifficulty: int, percentile=0.8):
        recipes = self.processed_df.copy()

        recipes = recipes[(recipes['cost'] <= maxPrice) &
                          (recipes['totalMinutes'] <= maxMinutes) &
                          (recipes['difficulty'] <= maxDifficulty)]

        C = recipes['cost'].mean()
        m = recipes['ratingValue'].quantile(percentile)

        q_recipes = recipes.copy().loc[recipes['ratingValue'] <= m]

        q_recipes = q_recipes.sort_values('ratingValue', ascending=False)

        q_recipes = q_recipes.head(10)

        # q_recipes['recipe'] = [
        #     f'recipe_{x}' for x in range(1, len(q_recipes) + 1)]

        recipes_indexes = q_recipes.index.to_list()
        raw_recipes = self.raw_df.iloc[recipes_indexes]

        q_recipes['url'] = raw_recipes['url']
        q_recipes['imageURL'] = raw_recipes['imageURL']
        q_recipes['title'] = raw_recipes['title']
        q_recipes['description'] = raw_recipes['description']

        # q_recipes = q_recipes.set_index('recipe')

        return q_recipes
