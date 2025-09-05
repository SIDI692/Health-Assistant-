from flask import Flask, render_template, request, redirect, url_for
import os
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)
HISTORY_FILE = "history.json"

# ===== Utilitaires =====
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {"IMC": []}

def save_history(data):
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def reset_history():
    data = {"IMC": []}
    save_history(data)

# ===== Routes =====
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/imc", methods=["GET", "POST"])
def imc():
    result = ""
    image = ""
    if request.method == "POST":
        try:
            poids = float(request.form["poids"])
            taille = float(request.form["taille"])
            imc_value = poids / (taille ** 2)
            history = load_history()
            history["IMC"].append(imc_value)
            save_history(history)

            if imc_value < 18.5:
                statut = "Maigreur"
                rec = "Nutrition: Augmente protéines et calories. Exercice: Renforcement musculaire."
                image = "maigreur.png"
            elif imc_value < 25:
                statut = "Normal"
                rec = "Nutrition: Maintiens équilibre. Exercice: Cardio 3x/semaine."
                image = "normal.png"
            elif imc_value < 30:
                statut = "Surpoids"
                rec = "Nutrition: Réduis sucres et graisses. Exercice: Marche 30 min/jour."
                image = "surpoids.png"
            else:
                statut = "Obésité"
                rec = "Nutrition: Suivi diététique obligatoire. Exercice: Activité physique régulière."
                image = "obesite.png"
            
            result = f"IMC={imc_value:.2f} | {statut}\n{rec}"
        except:
            result = "Erreur : Vérifie tes valeurs."
    return render_template("imc.html", result=result, image=image)

@app.route("/prediction", methods=["GET", "POST"])
def prediction():
    result = ""
    if request.method == "POST":
        try:
            age = int(request.form["age"])
            imc_value = float(request.form["imc"])
            diabete = request.form.get("diabete") == "oui"
            tension = request.form.get("tension") == "oui"
            asthme = request.form.get("asthme") == "oui"

            res = []
            if diabete or imc_value > 30 or age > 45:
                res.append("Risque Diabète: Élevé")
            else:
                res.append("Risque Diabète: Faible")

            if tension or imc_value > 28 or age > 50:
                res.append("Risque Hypertension: Élevé")
            else:
                res.append("Risque Hypertension: Faible")

            if asthme:
                res.append("Risque Asthme: Élevé")
            else:
                res.append("Risque Asthme: Faible")

            if imc_value < 18.5:
                conseil = "Nutrition: Augmenter protéines et calories. Exercice: Renforcement musculaire."
            elif imc_value < 25:
                conseil = "Nutrition: Maintenir équilibre. Exercice: Cardio 3x/semaine."
            elif imc_value < 30:
                conseil = "Nutrition: Réduire sucres et graisses. Exercice: Marche 30 min/jour."
            else:
                conseil = "Nutrition: Suivi diététique obligatoire. Exercice: Activité physique régulière."
            
            res.append("\nConseils: " + conseil)
            result = "\n".join(res)
        except:
            result = "Erreur : Vérifie tes valeurs."
    return render_template("prediction.html", result=result)

@app.route("/history")
def history():
    history_data = load_history()
    imc_values = history_data.get("IMC", [])

    graph_file = ""
    if imc_values:
        plt.figure(figsize=(4,3))
        plt.plot(imc_values, marker='o', color='blue')
        plt.title("Historique IMC")
        plt.xlabel("Mesures")
        plt.ylabel("IMC")
        plt.tight_layout()
        graph_file = "static/images/imc_history.png"
        plt.savefig(graph_file)
        plt.close()
    
    return render_template("history.html", imc_values=imc_values, graph_file=graph_file)

@app.route("/reset")
def reset():
    reset_history()
    return redirect(url_for('history'))

# ====== Run =====
if __name__ == "__main__":
    app.run(debug=True)

imc_value = poids / (taille ** 2)
if imc_value < 10 or imc_value > 70:
    raise ValueError("Valeur d'IMC irréaliste")