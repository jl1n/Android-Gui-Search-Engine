# Description:
Search engines  have become an essential part of the web, as they help organize and easily present pertinent information to users. General search engines such as Google allow users to search the entire web for information they need; however, more specific search engines, such as those built for Github, and Google Play, can specifically support developers by allowing them search for and learn from applications similar to those that they are attempting to build themselves. To contribute towards the goal of increasing tools available for mobile application developers this project proposes a new search engine for Android applications that uses information from apps’ Graphical User Interfaces as queries. The goal of this project will be to generate a web application with a simple interface that will rely on the Apache Lucene indexing engine to retrieve relevant applications that contain GUI layouts similar to those entered in a query. This project will use information from both open source and Google Play applications to extract component’s information from APKs.

# Project Setup:

Note that I am running this on openSUSE so the commands may be different depending on what flavor of Linux/Unix you may be using.

### Parse App XML Data:
1. Change the file path in XMLParser.java to the path to the directory with the app folders. The line to be changed looks like: File root = new File("/home/ExampleFilePath"); Note: the app folders in the directory specified shouldn't be nested in other folders
2. Compile and run the program: javac XMLParser.java then java XMLParser. 
3. 4 csv files (Application.csv, File.csv, Component.csv, Attrbutes.csv) will be created in the same directory to be read into the database

### Database setup:
1. Start the mysql server with "systemctl start mysql"
2. run the command: "mysql -u root create database guiSearch;"
3. cd into the directory that contains the databasedump.sql file (it's stored within the code_directory folder)
4. If your mysql server has no password, type in the following command: "mysql -u root [database_name] < databasedump.sql" otherwise, type in this command: "mysql -u root -p [database_name] < databasedump.sql"
5. You should now have a working copy of the latest database that we are running.
6. If you happen to want to add more data to the database from a csv file, you can run the following command: "mysqlimport --fields-terminated-by=, --verbose --local -u [user] -p [database] /path/to/address.csv"
7. If you happen to want to create a database dump of your own, simply run "mysqldump -u root -p [database_name] > dumpfilename.sql"

### Django setup:
Macs will need to install homebrew. To do this, enter: ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
1. To install Django, run "sudo pip install django" (sudo pip3 install django for mac)
2. To install scipy, run pip3 install scipy
3. Open a terminal window and run "sudo apt-get install python3-dev libmysqlclient-dev" ("brew install python3" and "brew install mysql" for macs)
4. Also run "sudo pip install mysqlclient", "sudo apt-get install gcc", "sudo pip install pysolr", and "sudo pip install django-haystack" ("brew install gcc48" and "sudo pip3 install pysolr" and "sudo pip3 install django-haystack" for macs)
5. If all of the above were successful, you can now cd into code_directory/guiSearch ( the directory that has the manage.py file) and run the command "python3 manage.py makemigrations" followed by "python3 manage.py migrate"
6. You can now run the command "python3 manage.py runserver" to get a server running at localhost:8000

### Solr Setup:
1. If you haven't made any changes to the database or to the search_indexes.py file, then you can skip straight to the last step
2. Changes to the database require you to run "python3 manage.py rebuild_index"
3. Changes to the search_indexes.py file require that you create a new schema with the command "python3 manage.py build_solr_schema > ../Android-GUI-Search-Engine/code_directory/solr-4.9.1/example/solr/collection1/conf/schema.xml" to create a new schema. Then, restart the solr server. After that, run the command from step 2 to rebuild the index.
4. run "java -jar ~/Android-GUI-Search-Engine/code_directory/solr-4.9.1/example/start.jar &" to start the solr search service in the background.

### Testing
1. Inside the code directory folder there is a folder labeled "TestingFiles", where there are various XML files from different apps. Some of the files are blank or intentionally invalid and are labeled as such. The majority of the other files are XML files from the Apps in the database. 
2. Once the server is running, and the user has navigated to the home screen at localhost:8000, they will be presented with a button to upload files, and a dropdown menu to search with the four algorithms. The differences in types of algorithms will be explained in another section. The default is "component search", so for the purposes of this explanation it will only focus on that.
3. User clicks "Browse..." and navigates to the the TestingFiles folder from the project folder, or their own testing folder. The user then chooses which files they would like to upload for comparison, and this simulates them uploading their application repository. Only XML files will be accepted. The way the search algorithms work is comparing the files, so the more files chosen, the longer it will take to search. 
4. The user clicks search, and waits for the results page to display. If they chose an incorrect type of file or invalid XML file, they are redirected to an error page, where they can return to the home screen. The results screen displays 25 apps at a time, in a table with the app name then a link to a popup showing the closest matching XML file, with the number of components in that file listed below. If there are multiple inputted XML files, there will be that many or less XML files displayed in the results.
5. User can return to home page for another search, or look through the XML files. 
6. An additional test that a user can run will test that solr is setup correctly and that they can load all of the view pages correctly. To do this, go to the directory with the manage.py file and type in "python3 manage.py test"

### Troubleshooting:


- One issue you may run into is that it says that your password for your mysql server is wrong. If so, cd into code_directory/guiSearch/guiSearch and edit the settings.py file where it says something like:  
DATABASES = {  
    'default': {  
    'ENGINE': 'django.db.backends.mysql',  
    'NAME': 'guiSearch',  
    'USER': 'root',  
    'PASSWORD': '1234',  
    'HOST': 'localhost',  
    'PORT': '3306',  
  }  
}  
and either change the password to whatever you set your mysql server's password to or get rid of the line completely (if you never set up a password for your mysql server). You may also need to change the NAME field depending on what you called your database. I believe the database dump should handle that part for you though.

# Django Directory Structure

Django's directories are a bit confusing I'll admit.

The structure looks something like:

guiSearch/  
|- manage.py  
|- guiSearch/  
&nbsp;&nbsp;&nbsp;&nbsp; |-  __init__.py  
&nbsp;&nbsp;&nbsp;&nbsp; |- settings.py  
&nbsp;&nbsp;&nbsp;&nbsp; |- urls.py  
&nbsp;&nbsp;&nbsp;&nbsp; |- wsgi.py  
|- searchEngine/  
&nbsp;&nbsp;&nbsp;&nbsp; |- __init__.py  
&nbsp;&nbsp;&nbsp;&nbsp; |- models.py  
&nbsp;&nbsp;&nbsp;&nbsp; |- views.py  
&nbsp;&nbsp;&nbsp;&nbsp; |- urls.py  
&nbsp;&nbsp;&nbsp;&nbsp; |- forms.py  
&nbsp;&nbsp;&nbsp;&nbsp; |- apps.py  
&nbsp;&nbsp;&nbsp;&nbsp; |- admin.py  
&nbsp;&nbsp;&nbsp;&nbsp; |- tests.py  
&nbsp;&nbsp;&nbsp;&nbsp; |- search_indexes.py
&nbsp;&nbsp;&nbsp;&nbsp; |- static/  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |- css/  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |- fonts/  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |- js/  
&nbsp;&nbsp;&nbsp;&nbsp; |- templates/  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |- searchEngine/  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  |- index.html  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  |- results.html  

So, searchEngine is the application that we are currently running on. The only time you should need to change anything that isn't in that folder is if you're adding a database (which you'd then use settings.py), adding some weburls (you'd want to edit both urls.py files), or you're adding another application.  

Within searchEngine, you can see that there are a number of crazy things going on. In models.py you can add new database models (like table schemas), or even models for forms.  

Then, within views.py you'll be doing all of the redirecting to various html pages and receiving things from the html inputs. You can also put any sort of python function into the views.py that you'd like to run when either input a file, or select an option, etc.  

urls.py is where you want to add some regular expressions to do some url redirects. For instance, if you type in localhost:8000/results.html (this won't actually work it's just an example), you should be able to add some line in urls.py (and in the other urls.py file) to make sure that when the results.html ending gets typed in it calls the results.html page.  

The directory static contains all of the css, fonts, and javascript that we could possible want. The style.css and results.css are files that I've created. The others are from bootstrap.  

The templates directory has all of the html that you need. You can link the css to the html files using some commands (examples are in both html files). 

The search_indexes.py file contains all of the things pertaining to indexing with Solr.
