#   ENG4000 - Capstone Project - Team A
##  Console Management System for Gaming Cafes 

### **Context**
---
Currently, Gaming Cafes are able to exercise a high degree of control over the computers that their customers can use. Some of these important functions include granting/revoking access to the computer, maintaining a time limit per customer, and the ability to gradually warn a customer of their time remaining. However, this control is limited to computers only. 

**Gaming Cafes are unable to exercise the same level of control over consoles.**

Our group aims to rectify this by creating a lightweight web application that will allow our users to control a network of smart switches, and track user information and metadata in a similar way to existing solutions.

### **Tech Stack**
* [Django](https://www.djangoproject.com/)
* [Kasa](https://github.com/python-kasa/python-kasa)

### **Getting Started**
---
Follow these steps to set up the project locally.

1. Make sure [*Python*](https://www.python.org/downloads/) is installed on your machine. This project requires version 3.0 or higher.
1. Create and run a [python virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) in the *project/ConsoleTracker* directory
2. Install the required dependencies

```
pip install -r requirements.txt
```
3. Start the web server locally. Please ensure the **SECRET_KEY** environmental variable is set properly.
```
python3 manage.py runserver
```

#### **Roadmap**
- [x] Barebones/Concept
    - [x] User is able to access the website
    - [x] User is able to select the machine they are using
    - [x] User is able to input an amount of time to add to their timer
    - [x] Able to connect to smart switches
- [ ] Minimal Viable Product
    - [ ] Expiring timer powers switch off
    - [ ] User data is stored in database (name, contact info, time)
    - [ ] When user is active, update time accordingly
- [ ] Release
    - [ ] UI/UX Improvements
    - [ ] Communicates with OPUS Software
    - [ ] Admin can grant/revoke access to computer
    - [ ] User authentication
    - [ ] Gradual warning system as time runs out
    - [ ] User can request to add time (outcome reflected front-end and back-end)

See the [***project board***](https://github.com/orgs/ENG4000-Team-A/projects/2) for a list of ongoing issues and improvements.

        
