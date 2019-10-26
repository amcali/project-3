from flask import Flask, render_template, request, redirect, url_for
from flask_uploads import UploadSet, IMAGES, configure_uploads
import pymongo 
import os
import re
from bson.objectid import ObjectId 


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


# Retrieving the environment variables
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = 'restaurant_reviews'
RESTAURANTS = 'restaurants'


# Creating the connection
conn = pymongo.MongoClient(MONGO_URI)


# Flask Routes Begin Here
@app.route('/')
def index():
    return render_template('index.html')


#Route to show existing restaurants in Mongo
@app.route('/restaurants')
def restaurants():
    """Fetch all the existing restaurants as a Python dictionary"""
    results = conn[DATABASE_NAME][RESTAURANTS].find({})
    """Fetch all images stored and return them"""
    all_images = conn[DATABASE_NAME]['image_url'].find({});
    """Return a template and assign the results to a placeholder in that template"""
    return render_template('restaurants.template.html', data=results, all_images=all_images)


#Route to show the 'create restaurant' form    
@app.route('/restaurant/new')
def create_new_restaurant():
    return render_template('new_restaurant.html')   

    
#Route to process the 'create restaurant' form
@app.route('/restaurant/new', methods=['POST'])
def process_new_restaurant():
    restaurant_name = request.form.get('restaurant_name')
    restaurant_address = request.form.get('restaurant_address')
    business_hours = request.form.get('business_hours')
    telephone = request.form.get('telephone')
    email_address = request.form.get('email_address')
    """get the uploaded image"""
    image = request.files.get('image')      
    """save uploaded image"""
    filename = images_upload_set.save(image)             


    """Saving created restaurant in MongoDB"""
    conn[DATABASE_NAME][RESTAURANTS].insert({
        'restaurant_name': restaurant_name,
        'restaurant_address': restaurant_address,
        'business_hours': business_hours,
        'telephone': telephone,
        'email_address': email_address,
        """save image url"""
        'image_url' : images_upload_set.url(filename) 
    })

    return redirect(url_for('index'))


"""Route to display a selected restaurant for updating"""
@app.route('/restaurant/<restaurant_id>/update')
def update_restaurant(restaurant_id):
    
    """Use MongoDB to find the object by id. We will receive the results as a dictionary using the find_one method"""
    result = conn[DATABASE_NAME][RESTAURANTS].find_one({
        '_id': ObjectId(restaurant_id)
    })
    """rendering template with existing information on selected restaurant"""
    return render_template('update_restaurant.html', data=result)
    


#Route to show an individual restaurant's reviews on a new page
@app.route('/reviews/<restaurant_id>')
def get_restaurant_reviews(restaurant_id):
    result = conn[DATABASE_NAME][RESTAURANTS].find_one({
        '_id': ObjectId(restaurant_id)
    })
    # print(result)
    return render_template("restaurant_reviews.html", result=result)    



#Flask "magic code" -- boilerplate
if __name__ == '__main__':
   app.run(host=os.environ.get('IP'),
           port=int(os.environ.get('PORT')),
           debug=True)

