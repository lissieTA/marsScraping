from flask import Flask, render_template, jsonify, redirect
import scrape_mars_flask
from flask_pymongo import PyMongo

# create instance of Flask app
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_scrape"
mongo = PyMongo(app)

mars = mongo.db.mars



#  create route that renders index.html template
@app.route("/")
def index():
    marsData = mongo.db.mars.find_one()
    return render_template("index.html", marsData=marsData)


@app.route("/scrape")
def scrape():
    
    mars_data = scrape_mars_flask.scrape()
    mars.update(
        {},
        mars_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)