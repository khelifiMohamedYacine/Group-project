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

The README file on GitHub has some minor differences to the one in our sprint 1 submission.  

### Our GitHub Repository:  
https://github.com/myk204-dev/Group-project

Google Drive Link (for working on our documentation and designs):  
https://drive.google.com/drive/folders/17ponXwzY-ukLank_L8885Snnm2IQpFjj?usp=drive_link

Trello Link (Kanban Board):  
https://trello.com/b/ISL0gIqD/my-trello-board


---

### How To Set Up And Use The App:
#### **Instructions for setting up the app locally:**  
A copy of our prototype source code has been included in this submission.
It can be found [here](./Technical%20Documents/Link%20To%20GitHub%20Repository.txt).  
(This is the 'Source_Code' folder located in 'Technical Documents').

Alternatively, you can download the source code from the 'main' branch of our GitHub repo (linked above).

Python, PIP and Django must be installed to run the application.  
Given that Python and PIP are present, Django can be installed using the command `python -m pip install Django`.    

#### **How to run the app (+ basic functionalities):**  
First, navigate to the source code directory within a command line/terminal. This should be the one containing 'manage.py'.  

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

#### **How to run the Django Tests:**  
There are seperate tests for each of our Djnago apps.  

Run the tests for the 'core_app' app using the command `python manage.py tests core_app`.

---

### Process Documents:
We have used the Trello website to create and maintain our Kanban board:  
https://trello.com/b/ISL0gIqD/my-trello-board

We have also taken regular snapshots of our Kanban board since 6/2/25, archiving them in the 'Kanban Board Archive' powerpoint'.  

We have kept a detailed record of our group meetings in the 'Group Meeting Record' document.  

---

### Technical Documents:
Our 'Architecture Overview' explains our web application's front-end, back-end, use of Django, and database structure.  

Our 'Testing Documentation' explains our Django unit tests and manual validation tests.  

---

### Product Documents:
Our 'Requirements Analysis' document contains our requirements/specification analysis.  

Our 'Design Plan' document contains our design plan.  

Our 'UI Mockups' powerpoint contains our UI mockup designs.  
