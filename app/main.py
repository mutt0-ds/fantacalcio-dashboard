from flask import Flask, jsonify,render_template, redirect, url_for, request
# from src.scraper import main
import json
import pandas as pd
app = Flask(__name__)


# @app.route('/', methods=['GET', 'POST'])
# def hello():
#     # players = main()
#     with open("static/test.json") as op:
#         players = json.load(op)
#     # testo = "<h1>Hello World!</h1><br><h2>My Team:</h2><br>"
#     # testo+="<br>".join(list(players.keys()))
#     return jsonify(players)

@app.route('/home', methods=['GET', 'POST'])
def home():
    with open("app/static/test.json") as op:
        players = json.load(op)
        df = pd.DataFrame.from_dict(players).T
        # df["news"] = ["\n".join(x) for x in df["news"]]
        html_df = df.to_html(index=False).replace('class="dataframe"','')
        
    # return render_template('test.html', title="home",table=html_df)
    #within app.route add the html page we are doing changes to
    return render_template("test.html", column_names=df.columns.values, row_data=list(df.values.tolist()),
                           link_column="SCHEDA GIOCATORE",news="NEWS", zip=zip)

@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)

#TODO: https://stackoverflow.com/questions/52644035/how-to-show-a-pandas-dataframe-into-a-existing-flask-html-table

# @app.route("/<major>/")
# def major_res(major):
#     course_list = list(client.db.course_col.find({"major": major.upper()}))
#     return flask.jsonify(**course_list)
