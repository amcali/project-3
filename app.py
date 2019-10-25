from flask import Flask, render_template, request, redirect, url_for
from flask_uploads import UploadSet, IMAGES, configure_uploads
import pymongo 
import os

app = Flask(__name__)

#configure uploads
TOP_LEVEL_DIR = os.path.abspath(os.curdir)
upload_dir = '/static/uploads/img/'
app.config["UPLOADS_DEFAULT_DEST"] = TOP_LEVEL_DIR + upload_dir
app.config["UPLOADED_IMAGES_DEST"] = TOP_LEVEL_DIR + upload_dir
app.config["UPLOADED_IMAGES_URL"] = upload_dir

images_upload_set = UploadSet('images', IMAGES)
configure_uploads(app, images_upload_set)
#end configure uploads

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
def index():
    return render_template('index.template.html')

#Route to show existing restaurants in Mongo
@app.route('/restaurants')
def restaurants():
    # Fetch all the existing todos as a Python dictionary
    results = conn[DATABASE_NAME][RESTAURANTS].find({})
    # Fetch all images stored and return them
    all_images = conn[DATABASE_NAME]['image_url'].find({}); #1
    #Return a template and assign the results to a placeholder in that template
    return render_template('restaurants.template.html', data=results, all_images=all_images)


#Route to show the 'add/create restaurant' form    
@app.route('/add_restaurant')
def add_restaurant():
    return render_template('add-restaurant.template.html')   



    
#Route to process the 'add/create restaurant' form
@app.route('/add_restaurant', methods=['POST'])
def process_add_restaurant():
    restaurant_name = request.form.get('restaurant_name')
    restaurant_address = request.form.get('restaurant_address')
    business_hours = request.form.get('business_hours')
    telephone = request.form.get('telephone')
    email_address = request.form.get('email_address')
    image = request.files.get('image') #1 -- get the uploaded image
    filename = images_upload_set.save(image) #2 -- save uploaded image    


    
    #Create a new restaurant
    conn[DATABASE_NAME][RESTAURANTS].insert({
        'restaurant_name': restaurant_name,
        'restaurant_address': restaurant_address,
        'business_hours': business_hours,
        'telephone': telephone,
        'email_address': email_address,
        'image_url' : images_upload_set.url(filename) #3 save image url
    })

    return redirect(url_for('index'))




# "magic code" -- boilerplate
if __name__ == '__main__':
   app.run(host=os.environ.get('IP'),
           port=int(os.environ.get('PORT')),
           debug=True)

