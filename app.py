from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
import pandas as pd

app = Flask(__name__)
app.secret_key = 'chiave sessioni'  # Chiave segreta per le sessioni
app.config['SECRET_KEY'] = 'questa è una chiave segreta'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False

csvPittori = "./static/PITTORI.csv"

def loadPittori(path):
    return pd.read_csv(path, sep=';')

pittoriDF = loadPittori(csvPittori)

def searchPittore(pittoriDf, keyword):
    #the CVS is structured as follow: Pittore;Numero libri
    #return Pittore; Numero libri associated to the keyword
    return pittoriDf[pittoriDf['Pittore'].str.contains(keyword, case=False)]

@app.route('/', methods = ['GET'])
def index():
    #load main page
    pittoriDF = loadPittori(csvPittori)
    return render_template('home.html')

@app.route('/search', methods = ['POST'])
def search():
    #search painter name and return number of associoated books
    keyword = request.form.get('pittore')
    #search
    resDF = searchPittore(pittoriDF, keyword)

    if resDF.empty:
        # Nessun risultato trovato
        return jsonify({"status": "error", "msg": "Nessun risultato trovato"})

    else:
        # Restituisci i risultati in formato JSON
        resJSON = resDF[['Pittore', 'Numero libro']].to_dict(orient='records')
        return jsonify({"status": "success", "data": resJSON})





if __name__ == '__main__':
    app.run(debug=True)