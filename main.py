from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
# from datetime import datetime 

with open('config.json', 'r') as c:
    params = json.load(c) ["params"]
local_server = True

app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password']
)
mail = Mail(app)
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)

# srno name email phone_num mes date
class Contacts(db.Model):

    srno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    mes = db.Column(db.String(80), nullable=False)
    # date = db.Column(db.String(12), nullable=True)

@app.route("/")
def home():
    return render_template('index.html', params=params)

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=="POST"):
       
        # "ADD ENTRY TO THE DATABASE"
         name = request.form.get('name')
         email = request.form.get('email')   
         phone = request.form.get('phone')
         message = request.form.get('message')  
        #  here we fetch the data from the database now lets add the data in the database 
         entry = Contacts(name=name, phone_num=phone, mes=message, email=email)
         db.session.add(entry)
         db.session.commit()
         mail.send_message('New message from '+ name,
          sender=email, 
          recipients=[params['gmail-user']],
          body= message + "\n" + phone
          )

    return render_template('contact.html', params=params)

@app.route("/about")
def about():
    return render_template('about.html', params=params)


@app.route("/post")
def post():
    return render_template('post.html', params=params)


app.run(debug=True,port=3000)