from flask import Flask, render_template,request,session,redirect
import secrets 


print(secrets.token_hex())


app = Flask(__name__)            

app.secret_key = secrets.token_hex()

@app.route("/achat",methods=['GET', 'POST'])     
def index(): 
    if request.method == 'POST':
        if request.form['chocolatine'] : 
            session['chocolatine'] = request.form['chocolatine']
        if request.form['croissant']: 
            session['croissant'] = request.form['croissant']     
        return redirect('/panier')
    return render_template('achat.html') 


@app.route("/panier",methods=['GET', 'POST'])     
def panier():        
        return render_template('panier.html')

@app.route("/viderpanier",methods=['GET', 'POST'])     
def supprimer():        
        session.pop('chocolatine', None)
        session.pop('croissant', None)
        return redirect('/panier')

if __name__ == "__main__":        # on running python app.py
    app.run()                     # run the flask app

