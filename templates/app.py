from flask import Flask, render_template
# Import scrape_mars
import scrape

from flask import Flask, render_template
# Import scrape_mars
import scrape

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
from flask_pymongo import PyMongo

# Create an instance of our Flask app.
app = Flask(__name__,template_folder='templates')

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
client = PyMongo(app)

# Set route
@app.route("/")
def index():
    mars_facts_data = client.db.mars_facts_data.find_one()
    return render_template("index.html", mars=mars_facts_data)

# Scrape 
@app.route("/scrape")
def scrape():
    mars_facts_data = client.db.mars_facts_data
    mars_data = scrape.scrape()
    mars.update({}, mars_data, upsert = True)
    return "scraped!"

if __name__ == "__main__":
    app.run(debug=True)