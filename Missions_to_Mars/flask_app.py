from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection locally 
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    try:
        # Find data from the mongo database
        mars_dict = mongo.db.mars_dict.find_one()
        # Return template and data
        return render_template("index.html", mars_dict=mars_dict)
    except:
        redirect("/scrape", code=302)

# Route for scrape function
@app.route("/scrape")
def scrape():

    # Run scrapped functions
    mars_dict = mongo.db.mars_dict
    mars_data = scrape_mars.scrape()
    mars_dict.update({}, mars_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)