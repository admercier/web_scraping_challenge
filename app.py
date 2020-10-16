import scrape_mars
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo

# Create an instance of Flask
app = Flask(__name__)

# Use pymongo to establish Mongo connection
conn = "mongodb://127.0.0.1:27017"
client = pymongo.MongoClient(conn)

#mongo = PyMongo(app, uri="mongodb://127.0.0.1:27017")

#define database and collection
db = client.mars_db
collection = db.items



#Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Find one record of data from the mongo database
    mars_data = collection.find_one()
    # Return template and data
    return render_template("index.html", mars_data = mars_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    result = scrape_mars.scrape_info()

    collection.insert_one(result)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
    