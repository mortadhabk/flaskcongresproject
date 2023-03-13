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

@app.route('/exoDico')
def exoDico():
   dic = {
     "John Wick":["John","Wick"], 
     "Piège de Cristal":["John","MaCLane"],
     "Terminator 2 : Le Jugement dernier":["John","Connor"],
     "Demolition Man":["John","Spartan"]}

   return render_template('afficher.html', dict=dic)

@app.route('/herit')
def templateHeritage():
    return render_template('templateEnfant.html')
if __name__ == "__main__":        # on running python app.py
    app.run()                     # run the flask app

