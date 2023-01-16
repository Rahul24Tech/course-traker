TechHub

  TechHub is a platform where user can upload new and trending or technology related video playlist where user can create his private or public video.
  
Setup:

 1. The first thing to do is to clone the repository:
  $ https://github.com/Rahul24pro/course-traker.git 
  $ cd course-traker

 2. Create a virtual environment to install dependencies in and activate it:
  $ virtualenv env
  $ source env/bin/activate

 3. Then install the dependencies:

  (env)$ pip install -r requirements.txt

 4. Note the (env) in front of the prompt. This indicates that this terminal session operates in a virtual environment set up by virtualenv2.

  Once pip has finished downloading the dependencies:

  (env)$ cd playlist
  (env)$ python3 manage.py runserver

 5. python version:- 3.8


Installation:
 
 1. pip install -r requirements. txt
 
 
Run Test:
 
 1.python3 manage.py runserver:- this will run at port:8000
 
Features:
  1. Added Favourite action to save particular course. 
  2. Added watch_later action to watch video later(some other days) of particular course.
  3. Added watch_later for particular playlist of a course i.e:- watch_later_playlist
  4. Added delete action for all favourite, watch_late, watch_later_playlist).


 
 
