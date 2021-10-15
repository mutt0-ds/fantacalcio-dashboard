from flask import Flask, render_template

import json
import pandas as pd

app = Flask(__name__)


@app.route("/home", methods=["GET", "POST"])
def home():
    with open("app/static/data_table.json") as op:
        players = json.load(op)
        df = pd.DataFrame.from_dict(players).T

    return render_template(
        "test.html",
        column_names=df.columns.values,
        row_data=list(df.values.tolist()),
        button="SCHEDA GIOCATORE",
        colonne_a_capo=["NEWS", "DATI"],
        zip=zip,
    )


@app.route("/")
def index():
    # giusto un check
    return "<h1>Server is Up</h1>"


# if __name__ == '__main__':
#     app.run(host="localhost", port=8000, debug=True)
