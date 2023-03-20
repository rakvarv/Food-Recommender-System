import foodrec_string_values as rec1
import foodrec_number_values as rec2
import numpy as np


def combine_results(foodrec1, foodrec2):
    result = []
    for i in range(len(foodrec2)):
        result.append((foodrec1[i][0], np.mean(
            [foodrec1[i][1], foodrec1[i][1], foodrec2[i]])))
    return result


def sort(combined_result, recipeTitles):

    # Sort the foods based on the cosine similarity scores
    result = sorted(combined_result, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar foods. Ignore the first food.
    result = result[len(recipeTitles):10+len(recipeTitles)]

    # Get the food indices
    food_indices = [i[0] for i in result]

    # Return the top 10 most similar foods

    return food_indices


def content_based_rec(titles: list):
    foodrec1_result = rec1.combined_rec_multiple_inputs(titles)
    foodrec2_result = rec2.meta_data_rec(titles)
    return sort(combine_results(foodrec1_result, foodrec2_result), titles)


#         UNCOMMENT THESE LINES TO TEST BY SIMPLY RUNNING THIS FILE
# input = ["Fiordilatte ice cream", "Chocolate cupcake",
#          "Baskets with shrimp and avocado"]
# foodrec1_result = rec1.combined_rec_multiple_inputs(input)
# foodrec2_result = rec2.meta_data_rec(input)
# print(sort(combine_results(foodrec1_result, foodrec2_result)))
