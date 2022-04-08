# Console Tracker :video_game:
A Console Management System for Gaming Cafes :coffee:

## Description
Currently, Gaming Cafes are able to exercise a high degree of control over the computers that their customers can use. Some of these important functions include granting/revoking access to the computer, maintaining a time limit per customer, and the ability to gradually warn a customer of their remaining time. However, this control is limited to computers only. Gaming Cafes are unable to exercise the same level of control over consoles such as Xbox, PlayStation and other gaming devices. Console Tracker aims to rectify this by providing a lightweight web application that will allow our users to control a network of smart switches, and track user information and metadata in a similar way to existing solutions.

## Prerequisites
||
|----|
|**1.** Install [Python](https://realpython.com/installing-python/). This project requires version 3.0 or higher|
|**2.** Install [Node.js](https://nodejs.org/en/). This project requires version 16 or higher|
|**3.** Set the environment variable `SECRET_KEY` to any value. This is used for [cryptographic signing](https://docs.djangoproject.com/en/dev/topics/signing/), so it is recommended to use a nontrival/generated value.
|**Optional:** In order to send SMS notifications, a [Twilio](https://www.twilio.com) account is required. Set the environment variables `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN` to the values found in your [account](https://www.twilio.com/console/account/settings).

## Run Instructions On Development Server
| *Steps* |
|----|
|**1.** Clone the repository |
|**2.** Create and run a [python virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) in the project directory |
|**3.** Download all the required libraries from [requirements.txt](https://github.com/ENG4000-Team-A/capstone-project/blob/main/project/requirements.txt) with the command  ```pip install -r requirements.txt```|
|**4.** Navigate into the [frontend](https://github.com/ENG4000-Team-A/capstone-project/tree/main/project/frontend) |
|**5.** Run the command ```npm install``` to download dependencies|
|**6.** Run the command ```npm start``` to start the react app|
|**7.** Open a new terminal and navigate into [Scripts](https://github.com/ENG4000-Team-A/capstone-project/tree/main/project/ConsoleTracker/ConsoleTrackerApp/scripts) then run ```./ServerSocket.py```|
|**8.** Open a new terminal and navigate into [Scripts](https://github.com/ENG4000-Team-A/capstone-project/tree/main/project/ConsoleTracker/ConsoleTrackerApp/scripts) then run ```./ExternalClientSocket.py```|
|**9.** Open a new terminal and navigate into [ConsoleTracker](https://github.com/ENG4000-Team-A/capstone-project/tree/main/project/ConsoleTracker) then run ```python manage.py runserver```|
|**10.** You should be able to access the [login page](http://localhost:3000/login)|

## Run Instructions For Tests
| *Steps* |
|----|
|**1.** Navigate into the [project](https://github.com/ENG4000-Team-A/capstone-project/tree/main/project/ConsoleTracker) directory then run ```python manage.py test ConsoleTrackerApp```|

## Run Instructions For Adding SSL Layer To Socket Scripts
| *Steps* |
|----|
|**1.** Navigate into the [frontend](https://github.com/ENG4000-Team-A/capstone-project/tree/main/project/frontend) directory then run ```set HTTPS=true && npm start```|
|**2.** Open a new terminal and naviagte into [frontend](https://github.com/ENG4000-Team-A/capstone-project/tree/main/project/frontend) directory then run the ```ssl_setup.bat``` script as administrator |

## Bug Reports
Please add any Bugs or Enhancements in the [Issues](https://github.com/ENG4000-Team-A/capstone-project/issues) of this Repository

        
