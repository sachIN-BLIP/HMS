from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_manager, LoginManager
from flask_login import login_required, current_user
from flask_mail import Mail
import json
from flask import Flask
from flask import Flask, render_template, request, redirect, flash, session, url_for
from CODE import NaiveBayes


# MY db connection
3.6
loc46al_server = True
app = Flask(__name__)
app.secret_key = 'aneeqah'


# this is for getting unique user access
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# SMTP MAIL SERVER SETTINGS

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME="add your gmail-id",
    MAIL_PASSWORD="add your gmail-password"
)
mail = Mail(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/databas_table_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/hmdbms'
db = SQLAlchemy(app)


# here we will create db models that is tables
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    usertype = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(1000))


class Patients(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    name = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    slot = db.Column(db.String(50))
    disease = db.Column(db.String(50))
    time = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    dept = db.Column(db.String(50))
    number = db.Column(db.String(50))


class Doctors(db.Model):
    did = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    doctorname = db.Column(db.String(50))
    dept = db.Column(db.String(50))


class Trigr(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    email = db.Column(db.String(50))
    name = db.Column(db.String(50))
    action = db.Column(db.String(50))
    timestamp = db.Column(db.String(50))


# here we will pass endpoints and run the fuction
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/doctors', methods=['POST', 'GET'])
def doctors():
    condition = "POST"
    mail = 'email'
    name = 'doctorname'
    d = 'dept'
    if request.method == condition:
        email = request.form.get(mail)
        doctorname = request.form.get(name)
        dept = request.form.get(d)
        insert_query_doctors(email, doctorname, dept)

    return render_template('doctor.html')


def insert_query_doctors(mail, name, d):
    query = db.engine.execute(
        f"INSERT INTO `doctors` (`email`,`doctorname`,`dept`) VALUES ('{mail}','{name}','{d}')")
    flash("Information is Stored", "primary")


@app.route('/patients', methods=['POST', 'GET'])
@login_required
def patient():
    doct = db.engine.execute("SELECT * FROM `doctors`")
    condition = "POST"
    mail = 'email'
    n = 'name'
    g = 'gender'
    s = 'slot'
    d = 'disease'
    t = 'time'
    da = 'date'
    de = 'dept'
    no = 'number'

    if request.method == condition:
        email = request.form.get(mail)
        name = request.form.get(n)
        gender = request.form.get(g)
        slot = request.form.get(s)
        disease = request.form.get(d)
        time = request.form.get(t)
        date = request.form.get(da)
        dept = request.form.get(de)
        number = request.form.get(no)
        subject = "HOSPITAL MANAGEMENT SYSTEM"
        insert_query_patient(email, name, gender, slot,
                             disease, time, date, dept, number)

    return render_template('patient.html', doct=doct)


def insert_query_patient(email, name, gender, slot, disease, time, date, dept, number):
    query = db.engine.execute(
        f"INSERT INTO `patients` (`email`,`name`,	`gender`,`slot`,`disease`,`time`,`date`,`dept`,`number`) VALUES ('{email}','{name}','{gender}','{slot}','{disease}','{time}','{date}','{dept}','{number}')")

    flash("Booking Confirmed", "info")


@app.route('/bookings')
@login_required
def bookings():
    em = current_user.email
    condtion = "Doctor"
    if current_user.usertype == condtion:
        query = db.engine.execute(f"SELECT * FROM `patients`")
        return render_template('booking.html', query=query)

    query = db.engine.execute(f"SELECT * FROM `patients` WHERE email='{em}'")
    return render_template('booking.html', query=query)


@app.route("/edit/<string:pid>", methods=['POST', 'GET'])
@login_required
def edit(pid):
    posts = Patients.query.filter_by(pid=pid).first()
    condition = "POST"
    mail = 'email'
    n = 'name'
    g = 'gender'
    s = 'slot'
    d = 'disease'
    t = 'time'
    da = 'date'
    de = 'dept'
    no = 'number'

    if request.method == condition:
        email = request.form.get(mail)
        name = request.form.get(n)
        gender = request.form.get(g)
        slot = request.form.get(s)
        disease = request.form.get(d)
        time = request.form.get(t)
        date = request.form.get(da)
        dept = request.form.get(de)
        number = request.form.get(no)
        update_queries(email, name, gender, slot, disease,
                       time, date, dept, number, pid)
        return redirect('/bookings')

    return render_template('edit.html', posts=posts)


def update_queries(email, name, gender, slot, disease, time, date, dept, number, pid):
    db.engine.execute(
        f"UPDATE `patients` SET `email` = '{email}', `name` = '{name}', `gender` = '{gender}', `slot` = '{slot}', `disease` = '{disease}', `time` = '{time}', `date` = '{date}', `dept` = '{dept}', `number` = '{number}' WHERE `patients`.`pid` = {pid}")

    flash("Slot is Updates", "success")


@app.route("/delete/<string:pid>", methods=['POST', 'GET'])
@login_required
def delete(pid):
    delete_query(pid)
    return redirect('/bookings')


def delete_query(pid):
    db.engine.execute(f"DELETE FROM `patients` WHERE `patients`.`pid`={pid}")
    flash("Slot Deleted Successful", "danger")


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    user = 'username'
    type = 'usertype'
    mail = 'email'
    passw = 'password'

    condition = "POST"
    if request.method == condition:
        username = request.form.get(user)
        usertype = request.form.get(type)
        email = request.form.get(mail)
        password = request.form.get(passw)
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist", "warning")
            return render_template('/signup.html')
        encpassword = generate_password_hash(password)

        signup_query(username, usertype, email, encpassword)

        return render_template('login.html')

    return render_template('signup.html')


def signup_query(username, usertype, email, encpassword):
    new_user = db.engine.execute(
        f"INSERT INTO `user` (`username`,`usertype`,`email`,`password`) VALUES ('{username}','{usertype}','{email}','{encpassword}')")
    flash("Signup Succes Please Login", "success")


@app.route('/login', methods=['POST', 'GET'])
def login():
    condtion = "POST"
    mail = 'email'
    passw = 'password'
    if request.method == condtion:
        email = request.form.get(mail)
        password = request.form.get(passw)
        user = User.query.filter_by(email=email).first()

        check = check_login_cred(user, password)
        if (check == 1):
            return redirect(url_for('index'))
        else:
            return render_template('login.html')

    return render_template('login.html')


def check_login_cred(user, password):
    if user and check_password_hash(user.password, password):
        login_user(user)
        flash("Login Success", "primary")
        return 1
    else:
        flash("invalid credentials", "danger")
        return 0


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul", "warning")
    return redirect(url_for('login'))


@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is Connected'
    except:
        return 'My db is not Connected'


@app.route('/details')
@login_required
def details():
    # posts=Trigr.query.all()
    posts = db.engine.execute("SELECT * FROM `trigr`")
    return render_template('trigers.html', posts=posts)


l1 = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain',
      'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 'spotting_ urination', 'fatigue',
      'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy', 'patches_in_throat',
      'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion',
      'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation',
      'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload',
      'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation',
      'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs', 'fast_heart_rate',
      'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps',
      'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails',
      'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain',
      'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side',
      'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)',
      'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic _patches',
      'watering_from_eyes', 'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances',
      'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption',
      'fluid_overload', 'blood_in_sputum', 'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling',
      'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze']


@app.route('/pred')
@login_required
def prediction():
    # NaiveBayes(psymptoms)
    posts = db.engine.execute("SELECT * FROM `trigr`")
    return render_template('pred.html', data=l1)


@app.route('/search', methods=['POST', 'GET'])
@login_required
def search():
    condition = "POST"
    s = 'search'
    if request.method == condition:
        query = request.form.get(s)
        dept = Doctors.query.filter_by(dept=query).first()
        name = Doctors.query.filter_by(doctorname=query).first()
        check_Doctor_Availability(name)
    return render_template('index.html')


def check_Doctor_Availability(name):
    if name:
        flash("Doctor is Available", "info")
    else:
        flash("Doctor is Not Available", "danger")


    return render_template('index.html')


@app.route('/pred', methods=["GET", "POST"])
def pred():
    if request.method == "POST":
        sym1 = request.form.get("s1")
        sym2 = request.form.get("s2")
        sym3 = request.form.get("s3")
        sym4 = request.form.get("s4")
        sym5 = request.form.get("s5")
        ans = NaiveBayes([sym1, sym2, sym3, sym4, sym5])
        print(sym1)
        print(ans)
        return render_template('result.html', data=ans)
    # print("hi")
    return render_template('pred.html', data=l1)


app.run(debug=True)











