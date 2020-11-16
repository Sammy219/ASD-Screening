from flask import Flask, render_template, url_for
from jinja2 import Template


app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/testpage")
def testpage():
    return render_template('testpage.html')

@app.route("/result")
def result():
    return render_template('result.html')

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)	
