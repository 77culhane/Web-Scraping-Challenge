#dependencies
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

#setup app
app = Flask(__name__)

#connect to PyMongo
mongo = PyMongo(app)

#create mongo database and intex.html file
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars 
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful"

if __name__ == "__main__":
    app.run(debug=True)