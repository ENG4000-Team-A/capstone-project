
# Console Tracker Configuration for Linux

## Dependencies
Python >= 3.8
Pip3
Ansible


## Ansible Installation
```
pip3 install ansible
```

## How to Run
```
ansible-playbook pi-book.yml --ask-become-pass --extra-vars "project_path=/your_path_to_project_here/capstone-project"

```

## Check Service Status
```
\# Check status of Django App
systemctl status ConsoleTracker

\# Check status of Nginx server
systemctl status nginx

```

Visit localhost/ for React App
Visit localhost:8000 for Django App
