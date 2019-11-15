from flask import Flask, render_template
# Import scrape_mars
import scrape_mars

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
from flask_pymongo import PyMongo

# Create an instance of our Flask app.
app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")



# Set route
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Scrape 
@app.route("/scrape")
def scrape():
    
    mars_dict = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_dict, upsert=True)

    return "scraped!"
 
if __name__ == "__main__":
    app.run(debug=True)