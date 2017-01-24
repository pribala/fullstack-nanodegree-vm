#Item Catalog Project

This project is a RESTful web application using the Python framework Flask along with implementing third-party OAuth 
authentication. The application uses the SQLAlchemy to perform CRUD operations to create, read, update and delete 
catalog items. SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers 
the full power and flexibility of SQL.
The application provides a list of items within a variety of categories as well as provides a user 
registration and authentication system. 
Registered users have the ability to post, edit and delete their own items. 
The templates are HTML pages with CSS for styling.

### Installation

Clone this repository using:

git clone https://github.com/pribala/fullstack-nanodegree-vm.git

### Using the Vagrant Virtual Machine

This project is done within the Vagrant virtual machine.The Vagrant VM has SQLite installed and configured, 
so that you don't have to install or configure them on your local machine.
To use the Vagrant virtual machine, navigate to the ~/fullstack-nanodegree-vm/vagrant/ directory in the 
terminal, then use the command vagrant up (powers on the virtual machine) followed by vagrant ssh 
(logs into the virtual machine).
Once you have executed the vagrant ssh command, you will want to cd /vagrant and cd catalog to change directory 
to the synced folders in order to test the project.
You'll need to have your VM on and be logged into it to run your database configuration file (database_setup.py), 
and start your web app using the application.py file.

### Using the database_setup.py and populate_database.py file

The database_setup.py file should be used for setting up your schema and database prior to use of the database 
for CRUD operations. This file needs to be run only once.
This file contains all the definitions for the python objects representing the underlying tables. Use the 
populate_database.py to populate the database with sample data.
Change to the catalog directory and run python database_setup.py and populate_database.py to build the database.

### Using the application.py

Running the application.py starts the web application at port 8000.
You can access the app from the browser using the url http://localhost:8000

You will be directed to the catalog page and can view the items under each category
by clicking on the listed category on the left pane of the browser. And clicking on each
item opens the item description page.

Only a logged in user can perform CRUD operations. 
The app implements third-party authentication & authorization service using Google Accounts and
Facebook. The login link takes  you to the login options (Google/ Facebook). Once logged in user can add, edit and 
delete items. The app also checks for the owner of each item and allows CRUD operations only to the creator of the 
items. The project implements a JSON endpoint that serves the same information as displayed in the HTML endpoints 
for an arbitrary item in the catalog.

### JSON Endpoints

To view the entire catalog as JSON: 
  * click the catalog link on the heading bar
  * visit the url localhost:8000/catalog

To view JSON for an item in the catalog
  * click the item detail link on the item details page
  * visit the url localhost:8000/item.json/<item-id>  

###What's Included

Within the repo you'll find the following directories and files:

  * /vagrant/catalog 
      * database_setup.py - this file is used to define the data objects.
      * populate_database.py -  this file is used to populate the database with sample data.
      * application.py -  this file defines the python modules for authentication, authorization and CRUD operations.
	                      
  * /templates 
      * catalog.html
	  * items.html
	  * item_details.html
	  * publiccatalog.html
	  * publicitems.html
	  * publicitem_details.html
	  * additem.html
	  * edititem.html
	  * deleteitem.html
	  * newcategory.html
  * /static 
      * main.css  

###Command line instructions to setup the database and run the application:

Navigate to /vagrant/catalog (after the VM is running and you are logged in). Then run the following commands

$python database_setup.py  
$python populate_database.py
$python application.py : starts the application at url 'http://localhost:8000'. 

###Reference:
  * Udacity's Working with CRUD course
  * FLASK Documentation
  * SQLAlchemy documentation
   