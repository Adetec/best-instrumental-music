# Best Instrumental Music Collection
## Udacity FSND project
### Overview
This app provides a list of items (music) within a variety of categories (musical genres) as well as provides a user registration and authentication system. Registered users will have the ability to post, edit and delete their own data records (Genres or music items).

### Techs used:
* Python3
* Flask
* SQLAlchemy
* Jinja2
* Google Aouth
* Materializecss
* JQuery
* ParticlesJS


### Requirements
1. [Virtual box](https://www.virtualbox.org): is the software that actually runs the virtual machine. Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.
**Ubuntu users**: If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center instead. Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.
2. [Vagrant](https://www.vagrantup.com/): Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. Install the version for your operating system.
**Windows users**: The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.
3. [Python3](https://www.python.org/download/releases/3.0/)
4. [SQLAlchemy](https://www.sqlalchemy.org/): Is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL. It provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language.
5. [Flask](https://flask.palletsprojects.com/en/1.0.x/): is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications. It began as a simple wrapper around Werkzeug and Jinja and has become one of the most popular Python web application frameworks.

### How to run the app?
1. After installing requirements, clone the Udacity [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm)
2. Open `vagrant` folder, clone this project inside.
3. `cd` into this project directory from your terminal.
4. Inside `vagrant`directory, run `vagrant up` to start running theVirtual machine, please note that it might take some time to download the OS system and apply the settings
5. After seeing the prompt come back, run `vagrant ssh` to log in.
6. cd into the `vagrant` directory by typing `cd /vagrant`
7. Move to this project directory _*by default `cd catalog`*_ and make sure you are in by running `ls` command to see the project files
8. Run `python3 database_setup.py`following by `python3 add_dummy_data.py` to create a database and add some dummy data
9. Finally run `python3 app.py`, to start running the server
10. Open the app on your browser at `http://localhost:5000` and have fun

### Accessing API Endpoints:
For each musical genre category or music item page, there's a linked button with Json API endpoint URI. For exemple:
* http://localhost:5000/JSON/v1/genre/1/music/1 **Pharaon** music item Json data is returned
* http://localhost:5000/JSON/v1/genres/1 **Flamenco** genre Json data is returned
* http://localhost:5000/JSON/v1/music **All music items** is returned
* http://localhost:5000/JSON/v1/genres **All musical genres** is returned