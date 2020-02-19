from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap
from haversine import haversine
import google.cloud
import googlemaps
import bcrypt
import pprint


app = Flask(__name__)

app.config['MONGO_DBNAME']='mongologinexample'
app.config['MONGO_URI']='mongodb://check:check@ds253587.mlab.com:53587/soda'

mongo = PyMongo(app)

bootstrap = Bootstrap()
bootstrap.init_app(app)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "THISISSECRET"

@app.route('/')
def index():
    if session.get('logged_in') and session.get('lat_long'):
        return render_template('loggedIndex.html', name=session['username'], lat = session['lat_long']['lat'], lng =session['lat_long']['lng'])

    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass , 'address' : request.form['address'], 'zipcode' : request.form['zipcode'], 'city' : request.form['city']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return render_template('signup.html', error = "That username is already taken")

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'name' : request.form['username']})

        if login_user:
            if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
                session['username'] = request.form['username']
                session['logged_in']=True

                address = login_user['address']
                city = login_user['city']
                zipcode = login_user['zipcode']
                totalQuery = "%s, %s, %s" % (address, city, zipcode)
                gmaps = googlemaps.Client(key='AIzaSyBpTKOfOdXY27Plw6m0OnhAixPIB7mD9xQ')
                session['lat_long'] = gmaps.geocode(totalQuery)[0]['geometry']['location']

                return redirect(url_for('index'))

        return 'Invalid username/password combination'
    return render_template('login.html')

@app.route('/registerPatient', methods=['GET', 'POST'])
def registerPatient():
    if session.get('logged_in'):
        if request.method == 'POST':
            if request.form['patientType']=='donor':
                donors = mongo.db.donors
                donors.insert({'hospital' : session['username'], 'name' : request.form['name'], 'height' : request.form['height'], \
                'weight' : request.form['weight'], 'age' : request.form['age'], 'bloodtype' : request.form['bloodtype'], 'gender': request.form['gender'], \
                'birthdate' : request.form['birthdate'], 'polyuria' : request.form['polyuria'], 'urine' : request.form['urine'], 'kidneyDisease' : request.form['kidneyDisease'], 'seizures' : request.form['seizures'], 'palpitations' : request.form['palpitations'], \
                'smoking' : request.form['smoking'], 'insomnia' : request.form['insomnia'], 'blurredVision' : request.form['blurredVision'], 'HIVHepa' : request.form['HIVHepa'], 'eyes' :request.form['patientEyes'], 'patientLungs' : request.form['patientLungs'], \
                'patientLungs' : request.form['patientLungs'], 'patientENT' : request.form['patientENT'], 'patientCardiovascular' : request.form['patientCardiovascular'], 'patientGastrointestinal' : request.form['patientGastrointestinal'], 'patientAllergic' : request.form['patientAllergic'], 'patientLymphatic' : request.form['patientLymphatic'], \
                'patientType' : request.form['patientType']})
            else:
                acceptors = mongo.db.acceptors
                acceptors.insert({'hospital' : session['username'], 'name' : request.form['name'], 'height' : request.form['height'], \
                'weight' : request.form['weight'], 'age' : request.form['age'], 'bloodtype' : request.form['bloodtype'], 'gender': request.form['gender'], \
                'birthdate' : request.form['birthdate'], 'polyuria' : request.form['polyuria'], 'urine' : request.form['urine'], 'kidneyDisease' : request.form['kidneyDisease'], 'seizures' : request.form['seizures'], 'palpitations' : request.form['palpitations'], \
                'smoking' : request.form['smoking'], 'insomnia' : request.form['insomnia'], 'blurredVision' : request.form['blurredVision'], 'HIVHepa' : request.form['HIVHepa'], 'eyes' :request.form['patientEyes'], 'patientLungs' : request.form['patientLungs'], \
                'patientLungs' : request.form['patientLungs'], 'patientENT' : request.form['patientENT'], 'patientCardiovascular' : request.form['patientCardiovascular'], 'patientGastrointestinal' : request.form['patientGastrointestinal'], 'patientAllergic' : request.form['patientAllergic'], 'patientLymphatic' : request.form['patientLymphatic'], \
                'patientType' : request.form['patientType'], 'organRequest' : request.form['organRequest']})

    return render_template('registerPatient.html')


@app.route('/donate', methods=['GET', 'POST'])
def donate():
    print "running"
    if request.method == 'POST':
        session['deadman'] = request.form['deadman']

    return render_template('donate.html')

@app.route('/patients')
def patients():
    acceptor_li = mongo.db.acceptors.find()
    mint=4
    for acceptor in acceptor_li:
        tempo=mongo.db.users.find_one({"name": acceptor["hospital"]})
        address = tempo["address"].encode('utf-8')
        city = tempo['city']
        zipcode = tempo['zipcode']
        totalQuery = "%s, %s, %s" % (address, city, zipcode)
        gmaps = googlemaps.Client(key='AIzaSyBpTKOfOdXY27Plw6m0OnhAixPIB7mD9xQ')
        tempo2 = gmaps.geocode(totalQuery)[0]['geometry']['location']
        a_hospital_tuple= (tempo2["lat"], tempo2["lng"] )
        d_hospital_tuple= (session['lat_long']["lat"], session['lat_long']["lng"] )

        distance_difference= haversine(d_hospital_tuple, a_hospital_tuple)

        donors = mongo.db.donors
        donor = donors.find_one({"name": session['deadman']})

        try:
            ah = float(acceptor["height"].encode('utf-8'))
            dh = float(donor["height"].encode('utf-8'))
            aw = float(acceptor["weight"].encode('utf-8'))
            dw = float(donor["weight"].encode('utf-8'))
            dh = float(donor["height"].encode('utf-8'))
            aa = float(acceptor["age"].encode('utf-8'))
            da = float(donor["age"].encode('utf-8'))
        except:
            return "No exist"

        height_difference= (ah-dh)/ah
        weight_difference= (aw-dw)/aw
        age_difference= (aa-da)/aa

        best_acceptor = ''

        if(acceptor["organRequest"].encode('utf-8')=="heart"):
            if("infect" in donor["patientCardiovascular"].encode('utf-8')):
                print("Donor can't donate a heart because of his heart health history/OR current Cardiovascular condition")
                #THIS PATIENT'S HEART IS NOT FIT FOR DONATION
            else:
                if (donor["bloodtype"].encode('utf-8')== acceptor["bloodtype"].encode('utf-8')):
                    suma=distance_difference+ height_difference + weight_difference + age_difference
                    if(suma<mint):
                        mint=suma
                        best_acceptor= acceptor["name"]

        if(acceptor["organRequest"].encode('utf-8')=="lungs"):
            if ("infect" in donor["patientLungs"].encode('utf-8') or donor["smoking"].encode('utf-8')=="yes"):
                print("Donor can't donate a lung because of his lung health history/OR current respiratory condition")
                exit()
                #THIS PATIENT'S lUNGS ARE NOT FIT FOR DONATION
            if (donor["bloodtype"].encode('utf-8') == acceptor["bloodtype"].encode('utf-8')):
                    suma=distance_difference+ height_difference + weight_difference + age_difference
                    if(suma<mint):
                        mint=suma
                        best_acceptor= acceptor["name"]

        statement = "They don't match!"

        if(acceptor["organRequest"].encode('utf-8')=="kidney"):
            if(donor["kidneyDisease"].encode('utf-8')=="yes" or donor["urine"].encode('utf-8')=="yes" or donor["Polyuria"].encode('utf-8')== "yes"):
                statement = "Donor can't donate a kidney because of his kidney history/OR current kidney condition"
                #THIS PATIENT'S KIDNEY IS NOT FIT FOR DONATION
            elif (donor["bloodtype"].encode('utf-8')== acceptor["bloodtype"].encode('utf-8')):
                suma=distance_difference+ height_difference + weight_difference + age_difference
                if(suma<mint):
                    mint=suma
                    best_acceptor= acceptor["name"].encode('utf-8')
                statement = "The deceased donor's " + acceptor["organRequest"]+ " has been matched with the acceptor patient " + best_acceptor + " !" + "The patient " + best_acceptor + " has been transferred the organ kidney and their life has been saved!"

        return render_template('saved.html', istatement = statement)

@app.route('/logout')
def logout():
    session.clear()
    session['logged_in']=False
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)
