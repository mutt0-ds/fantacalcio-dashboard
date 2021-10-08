from flask import Flask, render_template

import json
import pandas as pd# set configuration values

app = Flask(__name__)

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
                           button="SCHEDA GIOCATORE",colonne_a_capo=["NEWS","DATI"], zip=zip)

@app.route('/')
def index():
    return "<h1>Server is Up</h1>"

# if __name__ == '__main__':
#     app.run(host="localhost", port=8000, debug=True)
