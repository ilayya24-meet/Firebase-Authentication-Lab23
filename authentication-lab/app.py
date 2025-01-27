from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
config = {

  "apiKey": "AIzaSyB5bEovfbpVEFp_NCxritpB33FUlsse_0c",

  "authDomain": "meet24lab.firebaseapp.com",

  "projectId": "meet24lab",

  "storageBucket": "meet24lab.appspot.com",

  "messagingSenderId": "885302312908",

  "appId": "1:885302312908:web:e8972aafc751260a132769",

  "measurementId": "G-Q0HHEWW6PN",
  "databaseURL":"https://meet24lab-default-rtdb.firebaseio.com/"

};

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        username = request.form['username']
        bio = request.form['bio']


        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {'email': email, 'password': password, 'full_name': full_name, 'username': username, 'bio': bio}
            db.child("Users").child(UID).set(user)

            return redirect(url_for('add_tweet'))

        except:
           error = "Authentication failed"
    return render_template("signup.html")

    


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        try:
            UID = login_session['user']['localId']
            
            tweet = {
                'title':title, 'text':text, 'uid':UID
             }

            db.child("Tweets").push(tweet)
            return redirect(url_for('tweets'))
        except:
            error = "Authentication failed"
    return render_template("add_tweet.html")

@app.route('/all_tweets', methods=['GET', 'POST'])
def tweets():
    

    tweets = db.child("Tweets").get().val()

    return render_template("tweets.html", tweets=tweets)

if __name__ == '__main__':
    app.run(debug=True)