from flask import Flask, render_template, request, redirect, url_for
import pymongo
import os

app = Flask(__name__)

# 1. Retrieve the environment variables
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = 'restaurant_reviews'
RESTAURANTS = 'restaurants'

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

# Flask Routes Begin Here
@app.route('/')
def home():
    return render_template('index.template.html')


#Route to show the 'add/create restaurant' form    
@app.route('/add_restaurant')
def add_restaurant():
    return render_template('add-restaurant.template.html')   
    
#Route to process the 'add/create restaurant' form
@app.route('/add_restaurant', methods=['POST'])
def process_add_restaurant():
    restaurant_name = request.form.get('restaurant_name')
    restaurant_address = request.form.get('restaurant_address')
    
    #Create a new restaurant
    conn[DATABASE_NAME][RESTAURANTS].insert({
        'restaurant_name': restaurant_name,
        'restaurant_address': restaurant_address
    })

    return redirect(url_for('home'))

#Route to show created / added restaurants
@app.route('/restaurants')
def restaurants():
    # Fetch all the existing todos as a Python dictionary
    results = conn[DATABASE_NAME][RESTAURANTS].find({})
    #Return a template and assign the results to a placeholder in that template
    return render_template('restaurants.template.html', data=results)    



# "magic code" -- boilerplate
if __name__ == '__main__':
   app.run(host=os.environ.get('IP'),
           port=int(os.environ.get('PORT')),
           debug=True)

