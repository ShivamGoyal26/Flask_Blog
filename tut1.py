from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/about")
def about():
    var = "shivam"
    return render_template('about.html', name=var)

@app.route("/bootstrap")
def bootsrap():
    return render_template('bootstrap.html')

app.run(debug=True)