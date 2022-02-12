# Console Tracker
A Console Management System for Gaming Cafes

## Description
Currently, Gaming Cafes are able to exercise a high degree of control over the computers that their customers can use. Some of these important functions include granting/revoking access to the computer, maintaining a time limit per customer, and the ability to gradually warn a customer of their remaining time. However, this control is limited to computers only. Gaming Cafes are unable to exercise the same level of control over consoles such as Xbox, PlayStation and other gaming devices. Console Tracker aims to rectify this by providing a lightweight web application that will allow our users to control a network of smart switches, and track user information and metadata in a similar way to existing solutions.

## Run Instructions On Development Server
| *Steps* |
|----|
|**1.** Clone the repository |
|**2.** Install [Python](https://realpython.com/installing-python/). This project requires version 3.0 or higher|
|**3.** Create and run a [python virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) in the project directory |
|**4.** Download all the required libraries from [requirements.txt](https://github.com/ENG4000-Team-A/capstone-project/blob/main/project/requirements.txt) by the command  ```pip install -r requirements.txt```|
|**5.** Install [Node.js](https://nodejs.org/en/). This project requires version 16 or higher|
|**7.** Navigate into the [frontend](https://github.com/ENG4000-Team-A/capstone-project/tree/main/project/frontend) |
|**8.** Run the command ```npm start``` to start the react app|
|**9.** Open a new terminal and naviagte into [Scripts](https://github.com/ENG4000-Team-A/capstone-project/tree/main/project/ConsoleTracker/ConsoleTrackerApp/scripts) then run ```./ServerSocket.py```|
|**10.** Open a new terminal and naviagte into [Scripts](https://github.com/ENG4000-Team-A/capstone-project/tree/main/project/ConsoleTracker/ConsoleTrackerApp/scripts) then run ```./ExternalClientSocket.py```|
|**11.** You should be able to access the [login page](http://localhost:3000/login)|

## Run Instructions For Tests
| *Steps* |
|----|
|**1.** Navigate into the [project](https://github.com/ENG4000-Team-A/capstone-project/tree/main/project/ConsoleTracker) directory then run ```python manage.py test ConsoleTrackerApp```|

## Documentation
* [Agile Roadmap](https://github.com/ENG4000-Team-A/capstone-project/blob/main/documents/Agile%20Roadmap.pdf)

## Bug Reports
Please add any Bugs or Enhancements in the [Issues](https://github.com/ENG4000-Team-A/capstone-project/issues) of this Repository

        
