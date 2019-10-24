from flask import Flask, render_template, request, redirect, url_for
import pymongo
import os

app = Flask(__name__)

# Flask Routes Begin Here
@app.route('/')
def home():
    return render_template('index.template.html')

@app.route('/restaurants')
def restaurants():
    return render_template('restaurants.template.html')
    
@app.route('/add_restaurant')
def add_restaurant():
    return render_template('add-restaurant.template.html')    
    

# 1. Retrieve the environment variables
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = 'restaurant_reviews'

# 2. Create the connection
conn = pymongo.MongoClient(MONGO_URI)

# 3. Query
# doc = conn[DATABASE_NAME]["listingsAndReviews"].find({
#     'address.country':'Canada'
# }).limit(10)

# for d in doc:
#     print("Name:", d['name'])
#     print("Price: $", d['price'])
#     print('-------')

# "magic code" -- boilerplate
if __name__ == '__main__':
   app.run(host=os.environ.get('IP'),
           port=int(os.environ.get('PORT')),
           debug=True)

