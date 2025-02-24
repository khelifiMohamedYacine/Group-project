# Software Development Group Project

### Group Name: Syntax Squad 2

### Group Members:
1) Khelifi Mohamed Yacine (myk204-dev / yacine)
2) David Muoneke (DM7935-GH)
3) Renchengkun Wu (renchengkunwu)
4) Jerry Sharon Jenova Raju (jsharonjr)
5) Daniel Komarov (ZonateWhisper5)
6) Jonathan Young (JonathanY234)
7) Joshua Masih (jmasih1234)

### Our GitHub Repository:
https://github.com/myk204-dev/Group-project

Google Drive Link (for our documentation and designs):  
https://drive.google.com/drive/folders/17ponXwzY-ukLank_L8885Snnm2IQpFjj?usp=drive_link

Trello Link:  
https://trello.com/b/ISL0gIqD/my-trello-board


---

### How To Set Up And Use The App:
**Instructions for setting up the app locally:**  
A copy of our prototype source code has been included in this submission.
It can be found [here](./Technical%20Documents/Link%20To%20GitHub%20Repository.txt).  
(This is the 'Source_Code' folder located in 'Technical Documents').

Alternatively, you can download the source code from the 'main' branch of our GitHub repo (linked above).

Python, PIP and Django must be installed to run the application.  
Given that Python and PIP are present, Django can be installed using the command `python -m pip install Django`
(on UNIX systems, you may have to use `py` instead of `python`).  

**How to run the app (+ basic functionalities):**  
First, navigate to the source code directory within a command line/terminal. This should be the one containing 'manage.py'.  

Before running the application, use the command `python manage.py migrate` to apply all database migrations.

Run the web application using the command `python manage.py runserver`.  
If there are no problems, you should see the line "Starting development server at http://127.0.0.1:8000/".
This indicates that the application is running locally.  

Use the URL http://127.0.0.1:8000/ to visit the website (within a web browser).  
This default URL path will take you to the Create Account Page.  

The rest of the website should be reachable from here, but shortcuts are provided below:  
Login page - http://127.0.0.1:8000/login/  
Home page - http://127.0.0.1:8000/home/  
Jumping game - http://127.0.0.1:8000/jumping_game/  
Note that the Home page will appear slightly differently depending on whether or not you are logged in.  

**How to run the Django Tests:**  
There are seperate tests for each of our Djnago apps.  

Run the tests for the 'core_app' app using the command `python manage.py tests core_app`.

---

### Process Documents:
We have used the Trello website to create and maintain our Kanban board:  
https://trello.com/b/ISL0gIqD/my-trello-board

We have also taken regular snapshots of our Kanban board since 6/2/25, archiving them here:  
[insert link]

We have kept a detailed record of our group meetings here:    
[insert link]

---

### Technical Documents:
Our Architecture Overview explains our web application's front-end, back-end, use of Django, and database structure:    
[insert link]

Our Testing Documentation explains our Django unit tests and manual validation tests:    
[insert link]

---

### Product Documents:
Our Requirements Analysis documentation is here:  
[insert link]

Our Design Plan documentation is here:  
[insert link]

Our User Interface (UI) design mockups are here:  
[insert link]
