from flask import Flask, url_for, render_template
from flask import request, redirect, jsonify, flash
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from database_setup import Category, Item, Base, User
app = Flask(__name__)
from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog Application"

#Connect to Database and create database session
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create a new user
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# returns the user info given user id
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# returns user id given user email
def getUserId(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None	


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session.clear()
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# function for logging in with facebook account
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]


    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # see if user exists
    user_id = getUserId(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    flash("Now logged in as %s" % login_session['username'])
    return output


# function for disconneting from facebook
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"
	

# function for connecting using google account	
@app.route('/gconnect', methods=['POST'])
def gconnect():
    login_session['provider'] = 'google'
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    print result
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']

    # see if the user exists, if not add the user to the database
    user_id = getUserId(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id		
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    flash("you are now logged in as %s" % login_session['username'])
    return output


# function for disconnecting from google
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['credentials']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    return "You have been logged out"	
    if result['status'] == '200':
        #del login_session['credentials'] 
        #del login_session['gplus_id']
        #del login_session['username']
        #del login_session['email']
        #login_session.clear()		
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response	


@app.route('/')
def showCategories():
    # this function returns a list of all categories in the database and
    # the latest added item for each category
    try:
        categories = session.query(Category).order_by(Category.name.asc()).all()  # noqa
        message = ""
        items = []
    except NoResultFound:
        message = "There are no categories to display!"
        categories = []
    for category in categories:
        item = session.query(Item).filter_by(category_id=category.name).order_by(Item.last_modified.desc()).first()  # noqa
        if item != None:		
            details = item.title+' ('+category.name+')'
            items.append(details)
    if len(items) == 0:
        message = "There are no items to display!"
    # a different template is displayed depending on if the user is logged in 		
    if 'username' in login_session:		
        return render_template('catalog.html', categories=categories, message=message, items=items)  # noqa
    else:
        return render_template('publiccatalog.html', categories=categories, message=message, items=items)  # noqa	


@app.route('/catalog/newcategory', methods=['GET', 'POST'])
def newCategory():
    # this function adds a new category
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)
        flash('New Category %s Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newcategory.html')

		
@app.route('/catalog/<string:category_id>/items/')
def showItems(category_id):
    # this function displays the items for a given category
    try:	
        category = session.query(Category).filter_by(name=category_id).one()
        items = session.query(Item).filter_by(category_id=category_id)
        if session.query(Item).filter_by(category_id=category_id).count() != 0:
            message = ""
        else:
            message = "You currently have no items in this category"
    except NoResultFound:
        message = "Invalid category!"
        category = []
        items = []		
    categories = session.query(Category).order_by(Category.name.asc()).all()
    if 'username' in login_session:
        return render_template('items.html', category=category, items=items, categories=categories, message=message)  # noqa
    else:
        return render_template('publicitems.html', category=category, items=items, categories=categories, message=message)  # noqa	
	


@app.route('/catalog/<string:category_id>/<int:item_id>/')
def itemDetails(category_id, item_id):
    # this function displays the item description
    try:	
        item = session.query(Item).filter_by(id=item_id).one()
        creator = getUserInfo(item.user_id)
        message = ""
    except NoResultFound:
        message = "Invalid item!"
        item = []
    if 	'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicitem_details.html', item=item)		
    else:
        return render_template('item_details.html', item=item)	



@app.route('/catalog/newitem', methods=['GET','POST'])
def newItem():
    # this function adds a new item for a category
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newItem = Item(title=request.form['title'], description=request.form['description'], category_id=request.form['categoryid'], user_id=login_session['user_id'])
        session.add(newItem)
        flash('New Item %s Successfully Created' % newItem.title)
        session.commit()
        return redirect(url_for('showItems', category_id=newItem.category_id))
    else:
        categories = session.query(Category).order_by(Category.name.asc()).all()	
        return render_template('newitem.html', categories = categories)



@app.route('/catalog/<string:category_id>/<int:item_id>/edit', methods=['GET','POST'])
def editItem(category_id, item_id):
    # this function edits an item
    if 'username' not in login_session:
        return redirect('/login')
    item = session.query(Item).filter_by(id = item_id).one()
    creator = getUserInfo(item.user_id)	
    if login_session['user_id'] != creator.id:
        return render_template(url_for('showItems', category_id=item.category_id))
        flash('You are not authorized to edit this item. Only the item creater can edit the item.')		
    else:		
        if request.method == 'POST':
            title = request.form['title']	
            description = request.form['description']
            category_id = request.form['categoryid']
            if title != "":
                item.title = title        		
            if description != "":
                item.description = description
            if category_id != "":
                item.category_id = category_id
            session.add(item)
            session.commit()
            flash("Item Successfully Edited")		
            return redirect(url_for('showItems', category_id=item.category_id))
        else:
            categories = session.query(Category).order_by(Category.name.asc()).all()			
            return render_template('edititem.html', item=item, categories=categories)
           	


@app.route('/catalog/<string:category_id>/<int:item_id>/delete', methods=['GET','POST'])
def deleteItem(category_id, item_id):
    # this function deletes an item
    if 'username' not in login_session:
        return redirect('/login')
    item = session.query(Item).filter_by(id = item_id).one()
    creator = getUserInfo(item.user_id)	
    if login_session['user_id'] != creator.id:
        return render_template(url_for('showItems', category_id=item.category_id))
        flash("You can only delete items created by you!")		
    else:		
        if request.method == 'POST':
            session.delete(item)
            session.commit()
            flash("%s Successfully Deleted" %item.title)	
            return redirect(url_for('showItems', category_id=item.category_id))
        else:
            return render_template('deleteItem.html', item=item)


			
# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        login_session.clear()  # clear the login_session so user data does not persist		
        return redirect(url_for('showCategories'))
    else:
        login_session.clear()	
        flash("You were not logged in")
        return redirect(url_for('showCategories'))


# return JSON endpoint for items for each category
@app.route('/catalog')
def CatalogItemJSON():
    categories = session.query(Category).all()
    serializedCategories = []	
    for category in categories:
        serializedCategories.append(category.serialize)	
        cat = {}		
        items = session.query(Item).filter_by(category_id=category.name).all()
        serializedItems = []
        for item in items:
            serializedItems.append(item.serialize)
        cat['items'] = serializedItems			
        serializedCategories.append(cat)
    return jsonify(categories=[serializedCategories])		
 
 
if __name__ == '__main__':
    app.secret_key = 'very_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
