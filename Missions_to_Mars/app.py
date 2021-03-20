#Flask Application app.py

from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)


@app.route("/")
def index():
    mars_dict = client.mars.mars_dict.find_one()
    return render_template("index.html", mars_dict = mars_dict)

@app.route("/scrape")
def web_scrape():
    mars_dict=client.mars.mars_dict
    scraped_data = scrape_mars.scrape()
    mars_dict.update({},scraped_data, upsert = True)
    return redirect("/",code=302)


if __name__ == "__main__":
    app.run(debug = True)
