from flask import Flask, render_template,request

app = Flask(__name__)             # create an app instance

@app.route('/PageColoree',methods=['GET'])    
def set():
    nom = request.args.get("txt_name")
    prenom = request.args.get("txt_prenom")
    
    return render_template('template1.html', nom = nom ,prenom = prenom )

if __name__ == "__main__":        # on running python app.py
    app.run()                     # run the flask app


<html>
<head>
<title>
Changer la couleur de fond (résultat)
</title>
</head>
<body>
   <ul>
  <li> nom : {{nom }}</li>
   <li> prenom : {{prenom }}</li>
    </ul>

</body>
</html>





# boucle 
@app.route('/templateData', methods=['GET', 'POST'])
def tData():
    l =[1,3,7]
    dic = {"prenom":"John", "nom":"Wick"}
    return render_template('template2.html', list=l, dict=dic)

<ul>
  {% for nb in list %}
    <li>{{ nb }}</li>
  {% endfor %}
</ul>


 {% for k,v in dict.items() %}
        <li>{{ k }} & {{dict[k]}}</li>
      {% endfor %}

{% if name %}
  <h1>Hello {{ name }}!</h1>
{% else %}
  <h1>Hello, World!</h1>
{% endif %}