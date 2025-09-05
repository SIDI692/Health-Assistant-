<!DOCTYPE html>
<html>
<head>
    <title>Historique IMC</title>
</head>
<body>
<h1>Historique IMC</h1>

{% if imc_values %}
<p>Mesures :</p>
<ul>
    {% for v in imc_values %}
    <li>{{ "%.2f"|format(v) }}</li>
    {% endfor %}
</ul>

{% if graph_file %}
<h2>Graphique :</h2>
<img src="{{ url_for('static', filename='images/imc_history.png') }}" alt="Graphique IMC" width="400">
{% endif %}

{% else %}
<p>Aucune mesure enregistrée.</p>
{% endif %}

<br>
<a href="/reset">🔄 Réinitialiser Historique</a><br><br>
<a href="/">🏠 Retour au menu</a>
</body>
</html>