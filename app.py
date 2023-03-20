from flask import Flask, request, send_from_directory
from flask_cors import CORS, cross_origin
from preprocess import Preprocessor
from foodrec_entry import content_based_rec
import csv


preprocessor = Preprocessor('./data/giallozaferano_dataset.xlsx')
# preprocessor = Preprocessor(
#     '/Users/bendik/Documents/UiB/Master/INFO345/app/backend/data/giallozaferano_dataset.xlsx')
preprocessor.process()

app = Flask(__name__, static_folder="frontend/build", static_url_path="")
CORS(app)


@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, "index.html")


@app.route('/api/list', methods=["GET"])
@cross_origin()
def list_all_recipes():
    all_recipes_df = preprocessor.list_all()
    print(all_recipes_df)

    return all_recipes_df.to_json(orient="records")


@app.route('/api/recommend/knowledge', methods=["POST"])
@cross_origin()
def recommend_recipes_knowledge():
    req_json = request.get_json(force=True)
    price, minutes, difficulty = req_json['maxPrice'], req_json['maxMinutes'], req_json['maxDifficulty']

    recommendation_df = preprocessor.build_chart(price, minutes, difficulty)
    print(recommendation_df)

    return recommendation_df.to_json(orient="records")


@app.route('/api/recommend/content', methods=["POST"])
@cross_origin()
def recommend_recipes_content():
    req_json = request.get_json(force=True)
    recipeTitles = req_json['recipeTitles']

    recommendation_indeces = content_based_rec(recipeTitles)
    raw_df = preprocessor.raw_df

    recommendation_df = raw_df.iloc[recommendation_indeces]

    print(recommendation_df)

    return recommendation_df.to_json(orient="records")


@app.route('/api/submit', methods=["POST"])
@cross_origin()
def submit():
    recDict = {"A": "ContentBased", "B": "KnowledgeBased"}

    req_json = request.get_json(force=True)
    fromPage, answers, payload, recommendations = req_json['fromPage'], req_json[
        'answers'], req_json['payload'], req_json['recommendations']

    recSystem = recDict[fromPage]
    satisfaction = answers["satisfaction"]
    understanding = answers["understanding"]
    easeOfUse = answers["easeOfUse"]

    cost, experience, minutes, recipe1, recipe2, recipe3 = "null", "null", "null", "null", "null", "null",
    if fromPage == "A":
        recipe1, recipe2, recipe3 = payload["recipe1"], payload["recipe2"], payload["recipe3"]
    else:
        cost, experience, minutes = payload["cost"], payload["experience"], payload["minutes"]

    print(fromPage, answers)

    try:
        with open('./data/answers.csv', 'a', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(
                [fromPage, recSystem, satisfaction, understanding, easeOfUse, cost, experience, minutes, recipe1, recipe2, recipe3, recommendations])
    except:
        print("Something went wront when saving answers")

    return "OK"


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
