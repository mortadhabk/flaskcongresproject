from flask import Flask, render_template,request

app = Flask(__name__)             # create an app instance

def deb_HTML(titre):
    ret = "<HTML>\n"
    ret = ret + "<HEAD>\n "+"<TITLE>\n"+ titre+ "</TITLE>\n</HEAD>\n"
    ret = ret + "<BODY>\n"    
    return ret

def fin_HTML():
    fin = "\n</BODY>\n</HTML>\n"
    return fin
def page(titre,contenu):
    return deb_HTML(titre) + contenu + fin_HTML()



@app.route("/")                   # at the end point /
def base():
    return page("Page d'accueil","Bonjour")     # which returns "hello world"


@app.route("/saisieBorne")     
def index():              # at the end point /
    return render_template('saisieBorne.html') 

@app.route('/PageColoree',methods=['GET'])     
def set():       
    bornea = int(request.args.get("bornea"))
    borneb = int(request.args.get("borneb"))
    list = []
    for i in range(bornea,borneb+1) : 
           list.append(i)
    return render_template('afficher.html', borne = list) 


if __name__ == "__main__":        # on running python app.py
    app.run()                     # run the flask app

