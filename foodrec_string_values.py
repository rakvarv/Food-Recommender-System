#Import the relevant packages
import pandas as pd
import numpy as np

#Import dataframe and drop columns we won't use
df = pd.read_excel('./data/giallozaferano_dataset.xlsx')
df = df.drop(["prepTime", "cookTime", "fibers", "cholesterol", "sodium", "bestRating", "sugars", "proteins", "saturatedFat", "carbohydrates", "fat" ], axis=1)

# Import TfIdfVectorizer from the scikit-learn library
from sklearn.feature_extraction.text import TfidfVectorizer


def create_tfidf_matrix(feature, language, max_df = 1.0):
    # Define a TF-IDF Vectorizer Object. Remove all english stopwords and create useful word vectors
    tfidf = TfidfVectorizer(stop_words=str(language) if language != None else None, max_df=max_df)

    # Replace NaN with an empty string
    df[feature] = df[feature].fillna('')

    # Construct the required TF-IDF matrix by applying the fit_transform method on the overview feature
    tfidf_matrix = tfidf.fit_transform(df[feature])

    # Output the shape of tfidf_matrix
    tfidf_matrix.shape

    return tfidf_matrix

# Import linear_kernel to compute the dot product
from sklearn.metrics.pairwise import linear_kernel

def create_cosine_sim(tfidf_matrix):

    # Compute the cosine similarity matrix - this may take a few minutes
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    #Construct a reverse mapping of indices and food titles, and drop duplicate titles, if any
    indices = pd.Series(df.index, index=df['title'])

    return (cosine_sim, indices)

description_cosine_sim = create_cosine_sim(create_tfidf_matrix("description", "english"))
instructions_cosine_sim = create_cosine_sim(create_tfidf_matrix("instructions", None, 0.7))


# Content recommender based on single column
# Function that takes in food title, a single cosine_sim matrix and reverse mapping as input and gives recommendations 
def content_recommender(title, cosine_sim, indices, df = df): 
    # Obtain the index of the food that matches the title
    idx = indices[title]

    # Get the pairwise similarity scores of all foods with that food
    # And convert it into a list of tuples as described above
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the foods based on the cosine similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar foods. Ignore the first food.
    sim_scores = sim_scores[1:11]

    # Get the food indices
    food_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar foods
    return df['title'].iloc[food_indices]


# To use the ingredients column, we will need a different approach than TF-IDF, as every word has equal worth in a list of ingredients.
#The ingredients column is incorrectly formatted, so we need to fix that first

def fixformat(x):
    #convert ill-formatted string to list
    x = x[1:-1].split(", ")
    #Strip spaces and convert to lowercase
    return [str.lower(i.replace(" ", "")) for i in x]

df["ingredients"] = df["ingredients"].apply(fixformat)

# We need to convert the data to a soup before we can vectorize it
def create_soup(x):
    return ' '.join(x['ingredients'])

df['ingredients_soup'] = df.apply(create_soup, axis=1)

#getting cosine similarity using count vectorizer instead of TF-IDF
# Import CountVectorizer
from sklearn.feature_extraction.text import CountVectorizer

#Import cosine_similarity function
from sklearn.metrics.pairwise import cosine_similarity

def get_cosinesim_with_countvectorizer(feature):

    #Define a new CountVectorizer object and create vectors for the soup
    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(df[feature])

    #Compute the cosine similarity score (equivalent to dot product for tf-idf vectors)
    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    #create reverse mapping
    indices = pd.Series(df.index, index=df['title'])      #.drop_duplicates()

    return (cosine_sim, indices)

ingredients_cosine_sim = get_cosinesim_with_countvectorizer("ingredients_soup")


# Content recommender based on multiple columns
# Function that takes in food title as input and gives recommendations 
def get_sim_scores(title, cosine_sim, indices, df = df):
    # Obtain the index of the food that matches the title
    idx = indices[title]

    # Get the pairwise similarity scores of all foods with that food
    # And convert it into a list of tuples as described above
    sim_scores = list(enumerate(cosine_sim[idx]))

    return sim_scores

def combined_rec(title):
    description_sim = get_sim_scores(title, description_cosine_sim[0], description_cosine_sim[1])
    instructions_sim = get_sim_scores(title, instructions_cosine_sim[0], instructions_cosine_sim[1])
    ingredients_sim = get_sim_scores(title, ingredients_cosine_sim[0], ingredients_cosine_sim[1])

    result = []
    for index in range(len(description_sim)):
        result.append((description_sim[index][0], np.mean([description_sim[index][1], instructions_sim[index][1], ingredients_sim[index][1]])))

    
    # Sort the foods based on the cosine similarity scores
    result = sorted(result, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar foods. Ignore the first food.
    result = result[1:11]

    # Get the food indices
    food_indices = [i[0] for i in result]

    # Return the top 10 most similar foods
    return df['title'].iloc[food_indices]
    

def combined_rec_multiple_inputs(titles: list):

    description_sim = []
    instructions_sim = []
    ingredients_sim = []

    combined_features = {}

    
    for title in titles:
        combined_features[title] = []
        description_sim = get_sim_scores(title, description_cosine_sim[0], description_cosine_sim[1])
        instructions_sim = get_sim_scores(title, instructions_cosine_sim[0], instructions_cosine_sim[1])
        ingredients_sim = get_sim_scores(title, ingredients_cosine_sim[0], ingredients_cosine_sim[1])

        for i in range(len(description_sim)):
            combined_features[title].append(np.mean([description_sim[i][1], instructions_sim[i][1], ingredients_sim[i][1]]))
    
    result = combined_features[titles[0]]
    for i in range(len(result)):
        result[i] = (i, np.mean([combined_features[title][i] for title in titles]))

    return result

    # Sort the foods based on the cosine similarity scores
    #result = sorted(result, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar foods. Ignore the first food.
    #result = result[len(titles):10+len(titles)]

    # Get the food indices
    #food_indices = [i[0] for i in result]

    # Return the top 10 most similar foods

    #return df['title'].iloc[food_indices]

#print(combined_rec_multiple_inputs(['Pancakes with dacere syrup', 'Cocoa pancakes', 'Two-tone pancakes']))


