import pandas as pd
from scipy import spatial

df = pd.read_excel('./data/giallozaferano_dataset.xlsx')

df.insert(0, 'id', range(len(df)))

cost_cat_dic = {
    'Molto basso': '1',
    'Basso': '2',
    'Medio': '3',
    'Elevato': '4',
    'Molto elevata': '5'
}

diff_cat_dic = {
    'Molto facile': '1',
    'Facile': '2',
    'Media': '3',
    'Difficile': '4',
    'Molto difficile': '5'
}

df.replace({"cost": cost_cat_dic}, inplace=True)
df.replace({"difficulty": diff_cat_dic}, inplace=True)

# Remove non-numeric values and convert totalTime to integer datatype.
df["totalTime"] = df["totalTime"].str.extract('(\d+)', expand=False)
df["totalTime"] = pd.to_numeric(df["totalTime"], errors="coerce")
df["ratingCount"] = pd.to_numeric(df["ratingCount"], errors="coerce")

# Remove non-numeric values and convert prepTime & cookTime to integer datatype.
df["cookTime"] = df["cookTime"].str.extract('(\d+)', expand=False)
df["prepTime"] = df["prepTime"].str.extract('(\d+)', expand=False)
df["cookTime"] = pd.to_numeric(df["cookTime"], errors="coerce")
df["prepTime"] = pd.to_numeric(df["prepTime"], errors="coerce")

# Converting cost text categories in to numbers and performing numeric conversion on column
df["cost"] = pd.to_numeric(df["cost"], errors="coerce")
df["difficulty"] = pd.to_numeric(df["difficulty"], errors="coerce")

# df = df.dropna(subset=["cost"])

# Replacing all missing values with 0 and use the value 0
# as a mark to state that the amount of that certain feature is unknown
df["cholesterol"].fillna(0.1, inplace=True)
df["fibers"].fillna(0.1, inplace=True)
df["fat"].fillna(0.1, inplace=True)
df["saturatedFat"].fillna(0.1, inplace=True)
df["sodium"].fillna(0.1, inplace=True)
df["proteins"].fillna(0.1, inplace=True)
df["sugars"].fillna(0.1, inplace=True)
df["carbohydrates"].fillna(0.1, inplace=True)
df["calories"].fillna(0.1, inplace=True)
df["cookTime"].fillna(0.1, inplace=True)
df["ratingCount"].fillna(0.1, inplace=True)
df["ratingValue"].fillna(0.1, inplace=True)
df["totalTime"].fillna(0.1, inplace=True)
df["difficulty"].fillna(0.1, inplace=True)
df["cost"].fillna(0.1, inplace=True)


def meta_data_rec(dishes):

    unimp_features = df.loc[:, ["calories", "carbohydrates", "sugars", "proteins", "fat",
                            "saturatedFat", "fibers", "cholesterol", "sodium"]]

    dish_one_index = 0
    dish_two_index = 0
    dish_three_index = 0

    count = 0
    for dish in dishes:
        if count == 0:
            dish_one_index = df.index[df['title'] == dishes[0]].tolist()
            dish_one_index_value = dish_one_index[0]
            dish_one_row = unimp_features.iloc[dish_one_index_value]
            count += 1
        elif count == 1:
            dish_two_index = df.index[df['title'] == dishes[1]].tolist()
            dish_two_index_value = dish_two_index[0]
            dish_two_row = unimp_features.iloc[dish_two_index_value]
            count += 1
        elif count == 2:
            dish_three_index = df.index[df['title'] == dishes[2]].tolist()
            dish_three_index_value = dish_three_index[0]
            dish_three_row = unimp_features.iloc[dish_three_index_value]

    df_important = df.copy()
    df_unimportant = df.copy()

    for index, row in unimp_features.iterrows():
        for dish in dishes:
            df_unimportant.loc[index, "cos_1"] = 1 - \
                spatial.distance.cosine(dish_one_row, row)
            df_unimportant.loc[index, "cos_2"] = 1 - \
                spatial.distance.cosine(dish_two_row, row)
            df_unimportant.loc[index, "cos_3"] = 1 - \
                spatial.distance.cosine(dish_three_row, row)

    for index, row in df_unimportant.iterrows():
        cos_summed = (row["cos_1"] + row["cos_2"] + row["cos_3"])
        total_cos = cos_summed / 3
        df.loc[index, 'notimportscore'] = total_cos

    imp_features = df.loc[:, ["cost", "totalTime", "difficulty"]]

    count = 0
    for dish in dishes:
        if count == 0:
            dish_one_index = df.index[df['title'] == dishes[0]].tolist()
            dish_one_index_value = dish_one_index[0]
            dish_one_row = imp_features.iloc[dish_one_index_value]
            count += 1
        elif count == 1:
            dish_two_index = df.index[df['title'] == dishes[1]].tolist()
            dish_two_index_value = dish_two_index[0]
            dish_two_row = imp_features.iloc[dish_two_index_value]
            count += 1
        elif count == 2:
            dish_three_index = df.index[df['title'] == dishes[2]].tolist()
            dish_three_index_value = dish_three_index[0]
            dish_three_row = imp_features.iloc[dish_three_index_value]

    for index, row in imp_features.iterrows():
        for dish in dishes:
            df_important.loc[index, "cos_1"] = 1 - \
                spatial.distance.cosine(dish_one_row, row)
            df_important.loc[index, "cos_2"] = 1 - \
                spatial.distance.cosine(dish_two_row, row)
            df_important.loc[index, "cos_3"] = 1 - \
                spatial.distance.cosine(dish_three_row, row)

    for index, row in df_important.iterrows():
        cos_summed = (row["cos_1"] + row["cos_2"] + row["cos_3"])
        total_cos = cos_summed / 3
        df.loc[index, 'importscore'] = total_cos

    for index, row in df.iterrows():
        df.loc[index, 'totalscore'] = (
            row["importscore"] + row["importscore"] + row["notimportscore"]) / 3

    df["totalscore"].fillna(0, inplace=True)

    score_list = []
    for index, row in df.iterrows():
        score_list.append(row["totalscore"])

    return score_list

# print(meta_data_rec(dishes=dishes))
