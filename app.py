from flask import Flask, render_template, request, redirect, url_for
import pymongo
import os

app = Flask(__name__)

# Flask Routes Begin Here
@app.route('/')
def home():
    return render_template('index.template.html')
    
    # search_terms = request.args.get('search-by')
    # country = request.args.get('country')
    # must_have = request.args.getlist('must-have')
    
    # countries = ["Singapore", "Canada", "New Zealand", "Malaysia", "Ireland"]
    # amentities = ["Internet", "Washer", "Waterfront","Step-free access"]

    # search_criteria = {}
    # print (search_criteria)
    # if search_terms is not None and search_terms is not "":
    #     search_criteria["name"] = re.compile(r'{}'.format(search_terms), re.I)

    # if country != None and country != "Any":
    #     search_criteria['address.country'] = country 
        
    # if len(must_have) > 0:
    #     search_criteria['amenities'] = {
    #         '$all' : must_have 
    #     }    

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

