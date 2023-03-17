from flask import Flask, render_template,request,redirect,url_for

import sqlite3
import os
from sqlite3 import Error
from flask import session

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def connect_db(): 
    if not os.path.exists("bd.db"):
        print(f"Le fichier bd.db n'existe pas")
        connection = None
    else:         
        try:
            sqliteConnection = sqlite3.connect("bd.db")       
            print("Connection to SQLite réussi")
            return sqliteConnection
        except Error as e:
         print(f"The error {e} occured") 
def get_activites(sqliteConnection) :
    cursor = sqliteConnection.cursor()
    # Execute a SELECT statement to retrieve all records from the "activites" table
    cursor.execute('select * from congres')
    # Fetch all the results from the SELECT statement
    results = cursor.fetchall()
    cursor.close()
    return results

def get_participant(sqliteConnection) :

    cursor = sqliteConnection.cursor()
    # Execute a SELECT statement to retrieve all records from the "activites" table
    cursor.execute('select * from participants')
    # Fetch all the results from the SELECT statement
    results = cursor.fetchall()
    cursor.close()
    return results

def insert_participant(sqliteConnection,input_data) :
    cursor = sqliteConnection.cursor()

    # Execute a SELECT statement to retrieve all records from the "activites" table                                        
    cursor.execute("INSERT INTO PARTICIPANTS (CODESTATUT, NOMPART , PRENOMPART , ORGANISMEPART , CPPART , ADRPART , VILLEPART, PAYSPART, EMAILPART, DTINSCRIPTION) VALUES (?, ?, ?, ?,?, ?, ?, ?, ?,?)", (input_data["CODESTATUT"], input_data["NOMPART"],  input_data["PRENOMPART"],  input_data["ORGANISMEPART"],  input_data["CPPART"],  input_data["ADRPART"],  input_data["VILLEPART"],  input_data["PAYSPART"],  input_data["EMAILPART"],  input_data["DTINSCRIPTION"]))
    # Fetch all the results from the SELECT statement
    sqliteConnection.commit()
    cursor.close()
  
def verify_email(sqliteConnection,EMAILPART): 
    cursor = sqliteConnection.cursor()

    # Execute a SELECT statement to retrieve all records from the "activites" table                                        
    cursor.execute("select * from PARTICIPANTS  where PARTICIPANTS.EMAILPART = ? ",[EMAILPART])
    # Fetch all the results from the SELECT statement
    results = cursor.fetchall()
    cursor.close()
    if results :
        return True
    else :
        return False


def searchparticipant(sqliteConnection,EMAILPART): 
    cursor = sqliteConnection.cursor()

    # Execute a SELECT statement to retrieve all records from the "activites" table                                        
    cursor.execute("select C.CODCONGRES,C.TITRECONGRES,T.NOMTHEMATIQUE  from PARTICIPANTS as P, INSCRIRE as I ,CONGRES as C ,THEMATIQUES as T ,TRAITER as TR where P.CODPARTICIPANT = I.CODPARTICIPANT AND I.CODCONGRES = C.CODCONGRES AND TR.CODCONGRES = C.CODCONGRES AND T.CODETHEMATIQUE = TR.CODETHEMATIQUE AND P.EMAILPART = ? ",[EMAILPART])
    # Fetch all the results from the SELECT statement
    results = cursor.fetchall()
    cursor.close()
    return results


def querythematique(sqliteConnection): 
    cursor = sqliteConnection.cursor()

    # Execute a SELECT statement to retrieve all records from the "activites" table                                        
    cursor.execute("select T.CODETHEMATIQUE, T.NOMTHEMATIQUE from THEMATIQUES as T")
    # Fetch all the results from the SELECT statement
    results = cursor.fetchall()
    cursor.close()
    return results

def queryActivite(sqliteConnection): 
    cursor = sqliteConnection.cursor()

    # Execute a SELECT statement to retrieve all records from the "activites" table                                        
    cursor.execute("SELECT A.CODEACTIVITE,A.NOMACTIVITE FROM ACTIVITES as A ")
    # Fetch all the results from the SELECT statement
    results = cursor.fetchall()
    cursor.close()
    return results

def insert_congres(sqliteConnection,input_data) :
    try:
            
    
        cursor = sqliteConnection.cursor()
        # Execute a SELECT statement to retrieve all records from the "activites" table                                 
        cursor.execute("INSERT INTO CONGRES (TITRECONGRES, NUMEDITIONCONGRES , DTDEBUTCONGRES , DTFINCONGRES , URLSITEWEBCONGRES) VALUES (?, ?, ?, ?,?)", (input_data["TITRECONGRES"], input_data["NUMEDITIONCONGRES"],  input_data["DTDEBUTCONGRES"],  input_data["DTFINCONGRES"],  input_data["URLSITEWEBCONGRES"]))
        # Fetch all the results from the SELECT statement
        sqliteConnection.commit()

        cursor.execute("select last_insert_rowid()")
        
        cod_congres = cursor.fetchone()[0]
        for item in input_data["codeactivites"] :
            cursor.execute("INSERT INTO PROPOSER (CODEACTIVITE,CODCONGRES) VALUES (?, ?)", (item, int(cod_congres)))   
            sqliteConnection.commit()

        for item in input_data["codethematiques"] :
            cursor.execute("INSERT INTO TRAITER (CODCONGRES,CODETHEMATIQUE) VALUES (?, ?)", (int(cod_congres), item))
            sqliteConnection.commit()
        cursor.close()
        return True
    except :
        return False
def GetUsernameCode(sqliteConnection,username) :
         cursor = sqliteConnection.cursor()
        # Execute a SELECT statement to retrieve all records from the "activites" table  
         cursor.execute("select * from PARTICIPANTS  where PARTICIPANTS.EMAILPART = ? ",[username])
        # Fetch all the results from the SELECT statement
         results = cursor.fetchall()
         return results[0][0]  

def inserer_inscrire(sqliteConnection,congresselectionner,username) :
    try:
        cursor = sqliteConnection.cursor()
        userid = GetUsernameCode(sqliteConnection,username)
        print(f'userId : {userid}')
        cursor.execute("INSERT INTO INSCRIRE (CODPARTICIPANT,CODCONGRES) VALUES (?, ?)", (userid,congresselectionner))
        # Fetch all the results from the SELECT statement
        sqliteConnection.commit()
        cursor.close()
        return True
    except  :

        return False       

 #q 13
def list_activité_inscrire(sqliteConnection, codecongre) :
    try:
        cursor = sqliteConnection.cursor()
        # Execute a SELECT statement to retrieve all records from the "activites" table  
        cursor.execute("select  a.codeactivite ,a.NOMACTIVITE, c.CODCONGRES  from activites as a , congres as c, proposer as pr where   a.CODEACTIVITE = pr.CODEACTIVITE and pr.CODCONGRES = c.CODCONGRES and c.CODCONGRES = ? group by a.NOMACTIVITE",[codecongre])
        # Fetch all the results from the SELECT statement
        results = cursor.fetchall()
      
        cursor.close()
        return results
    except :
        return False  


    #q 13
def list_thematique_inscrire(sqliteConnection,codecongre) :
    try:
        cursor = sqliteConnection.cursor()
        # Execute a SELECT statement to retrieve all records from the "activites" table  
        cursor.execute("select th.CODETHEMATIQUE , th.NOMTHEMATIQUE, c.CODCONGRES from inscrire as i , congres as c , traiter as t ,thematiques as th where   c.CODCONGRES = t.CODCONGRES and t.CODETHEMATIQUE = th.CODETHEMATIQUE   and c.CODCONGRES = ? group by th.CODETHEMATIQUE",[codecongre])
        # Fetch all the results from the SELECT statement
        results = cursor.fetchall()
      
        cursor.close()
        return results
    except :
        return False    


def insert_choix_activite(sqliteConnection,codecongres,codeactivites,username) :
    try:
            
    
        cursor = sqliteConnection.cursor()
        userid = GetUsernameCode(sqliteConnection,username)
        cursor.execute("INSERT INTO choix_activites (CODEACTIVITE,CODPARTICIPANT,CODCONGRES) VALUES (?, ?,?)", (codeactivites,userid,codecongres))
        sqliteConnection.commit()
        cursor.close()
        return True
    except :
        return False       

def insert_choix_thematique(sqliteConnection,CODCONGRES,CODETHEMATIQUE,username) :
    try:
        cursor = sqliteConnection.cursor()
        userid = GetUsernameCode(sqliteConnection,username)
        cursor.execute("INSERT INTO choix_thematiques (CODETHEMATIQUE,CODPARTICIPANT,CODCONGRES) VALUES (?, ?,?)", (CODETHEMATIQUE,userid,CODCONGRES))
        sqliteConnection.commit()
        cursor.close()
        return True
    except :
        return False       
    
def show_choix_activities(sqliteConnection,username) : 
        cursor = sqliteConnection.cursor()
        cursor.execute("select a.CODEACTIVITE, a.NOMACTIVITE from participants p , choix_activites ca , activites a , congres c where p.CODPARTICIPANT = ca.CODPARTICIPANT and ca.CODEACTIVITE = a.CODEACTIVITE and ca.CODCONGRES = c.CODCONGRES and p.emailpart =? ",[username])
        results = cursor.fetchall()

        cursor.close()
        return results
def show_choix_thematiques(sqliteConnection,username) : 
        cursor = sqliteConnection.cursor()
        cursor.execute("select t.NOMTHEMATIQUE from participants p , choix_thematiques ct , thematiques t , congres c where p.CODPARTICIPANT = ct.CODPARTICIPANT and ct.CODETHEMATIQUE = T.CODETHEMATIQUE and ct.CODCONGRES = c.CODCONGRES and p.emailpart = ?", [username])
        results = cursor.fetchall()
        cursor.close()
        return results

def prixtotal(sqliteConnection,codecongre, tupleactivites,username) :
    try:
        cursor = sqliteConnection.cursor()
        params = [username, codecongre]

        # loop over the elements in tupleactivites and add them to the parameters list
        for element in tupleactivites:
           params.append(int(element[0]))
        query = "SELECT c.titrecongres, T.MONTANTTARIF+sum(a.PRIXACTIVITE+a.PRIXACTACCOMPAGNANT) as prix FROM tarifs t , statuts cs , participants p , congres c, PROPOSER pr , activites a  where p.codestatut = cs.codestatut and cs.codestatut = t.CODESTATUT and t.CODCONGRES = c.CODCONGRES and p.EMAILPART = ? and c.CODCONGRES = ? and c.codcongres = pr.codcongres and pr.codeactivite = a.CODEACTIVITE and a.CODEACTIVITE in ({}) group by c.codcongres".format(','.join(['?']*len(tupleactivites)))

        cursor.execute(query,params)
        results = cursor.fetchall()
        print(f'results {results}')
        cursor.close()
        return results
    except Error as e:
        print(e)    
    
def listactivitechoisir(sqliteConnection, tupleactivites) :
    try:
        cursor = sqliteConnection.cursor()
        params = []

        # loop over the elements in tupleactivites and add them to the parameters list
        for element in tupleactivites:
           params.append(element[0])
        query = "SELECT a.NOMACTIVITE  FROM  activites a where  a.CODEACTIVITE in ({}) ".format(','.join(['?']*len(tupleactivites)))

        cursor.execute(query,params)
        results = cursor.fetchall()
        print(results)
        cursor.close()
        return results
    except Error as e:
        print(e)    
def listthematiquechoisir(sqliteConnection, thematique) :
    try:
        cursor = sqliteConnection.cursor()
        params = []
    
        # loop over the elements in tupleactivites and add them to the parameters list
        for element in thematique:
           params.append(element[0])
        print(f'thematique {thematique}')
        query = "SELECT t.NOMTHEMATIQUE   FROM  thematiques t where  t.CODETHEMATIQUE in ({}) ".format(','.join(['?']*len(thematique)))

        cursor.execute(query,params)
        results = cursor.fetchall()
        print(results)
        cursor.close()
        return results
    except Error as e:
        print(e)    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/listcongres')
def page():
  
    congres = get_activites(connect_db())
    return render_template('listcongres.html',congres = congres)

@app.route('/listparticipants')
def listparticipants():
  
    participants = get_participant(connect_db())
    return render_template('listparticipants.html',participants = participants)

@app.route('/formulaire')
def formulaire():

    return render_template('formulaire.html')

@app.route('/enregistrer',methods=['POST'])
def enregistrer():
   try : 

    input_data  = {}
    for key, value in request.form.items():
        input_data[key] = value
    if not verify_email(connect_db(),input_data["EMAILPART"]) :

        insert_participant(connect_db(),input_data)
        return render_template('index.html',success = "le participant a été bien enregistrer." )
    return render_template('formulaire.html',error = "This Email exist." )

   except NameError:
          print(f"An exception occurred :{NameError} ")
 
@app.route('/saisieMail')
def saisieMail():

    return render_template('SaisieMail.html')
       
# select p.NOMPART, a.NOMACTIVITE,c.TITRECONGRES  from participants p , choix_activites ca , activites a , congres c 
# where p.CODPARTICIPANT = ca.CODPARTICIPANT and ca.CODEACTIVITE = a.CODEACTIVITE and ca.CODCONGRES = c.CODCONGRES and p.emailpart = 'mortadhaboubaker12@gmail.com'
@app.route('/search')
def search():
    
    mail = request.args.get('EMAILPART')
    participants = searchparticipant(connect_db(),mail)
    return render_template('ListInscription.html',participants=participants)
       
@app.route('/creercongres')
def creercongres():
    thematiques = querythematique(connect_db())
    activites = queryActivite(connect_db())
    data = {
        'thematiques' : thematiques,
        'activites' : activites
    }
    return render_template('creercongres.html' ,data = data)
       

@app.route('/enregistrercongres',methods=['POST'])
def enregistrercongres():
    input_data  = {}
    for key, value in request.form.items():
        input_data[key] = value
    input_data['codethematiques'] = request.form.getlist('codethematiques')
    input_data['codeactivites'] = request.form.getlist('codeactivites')

    checkinsert = insert_congres(connect_db(),input_data)
    if (checkinsert) : 
        return render_template('congresenregistree.html',item = input_data)
    return render_template('congresenregistree.html')

@app.route('/congresenregistree')
def congresenregistree():
    
    return render_template('congresenregistree.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return render_template('index.html', success = 'vous êtes déjà connecté')


    if request.method == 'POST':
        if(verify_email(connect_db(),request.form['EMAILPART'])): 
         session['username'] = request.form['EMAILPART']
         return render_template('index.html', success = 'vous êtes connecté')
        else : 
            return render_template('login.html',error = "This Email exist." )
    return render_template('login.html')

@app.route('/inscrire', methods=['GET', 'POST'])
def inscrire():
   if 'username' in session:
    
    if request.method == 'POST':
            congresselectionner = request.form['congres']
            username = session['username']
            session['codecongre'] = congresselectionner
            return redirect(url_for('choixactivite'))

    congres = get_activites(connect_db())
    return render_template('inscrire.html',congres = congres)
   return redirect(url_for('login'))

@app.route('/choixactivite', methods=['GET', 'POST'])
def choixactivite():
   if 'username' in session:
    error = request.values.get('error')
    username = session['username']
    codecongre = session['codecongre']
    if request.method == 'POST':

        session['activites'] = request.form.getlist('activites')
        session['thematiques'] = request.form.getlist('thematiques')
        prixtotals = prixtotal(connect_db(),codecongre, session['activites'] ,username)
        activity = listactivitechoisir(connect_db(),session['activites'] )
        thematique = listthematiquechoisir(connect_db(),session['thematiques'] )
        print(f'thematique : {thematique}')
        result = {'prixtotal' : prixtotals ,'activity' :activity, 'thematique' : thematique }

     
        return render_template('alllist.html',data= result )
    listactivite =  list_activité_inscrire(connect_db(),codecongre)
    listthematique =  list_thematique_inscrire(connect_db(),codecongre)
    
    list = {'listactivite' :listactivite,'listthematique' : listthematique  }
    return render_template('choixactivite.html',list = list,error = error)  

   return redirect(url_for('login'))
@app.route('/addlists', methods=['GET', 'POST'])
def addlists():
   if request.method == 'POST':
        inserer_inscrire(connect_db(),session['codecongre'],session['username'])  

        for item in session['activites']  : 
            tuplelist = eval(item)
            print(tuplelist)
            insert_choix_activite(connect_db(),session['codecongre'],tuplelist,session['username'])
        for item in session['thematiques'] :    
            tuplelist = eval(item)
            insert_choix_thematique(connect_db(),session['codecongre'],tuplelist,session['username'])

        session.pop('codecongre', None)
        session.pop('activites', None)
        session.pop('thematiques', None)

        return render_template('index.html',success = 'vous etes inscrit ')
   return render_template('index.html')


@app.route('/logout')
def logout():
        
        session.pop('username', None)
        return render_template('index.html',success = 'vous êtes deconnecté')

if __name__ == '__main__':
    app.run()