# REMPLR - *Replenish your meals!*

Meal Plan Creator is a web application that allows nutritionists to create personalized meal plans and grocery lists for their clients. This project is built with Python Flask framework, wtforms for form validation, and PostgreSQL database, using SQLAlchemy to connect to the database. The front-end is based on JavaScript.
![Screenshot 2023-04-20 at 8 54 24 AM](https://user-images.githubusercontent.com/87880250/233420912-15feab4c-2985-4e1e-af0f-3b7a38060cf6.png)



## Features
Authentication system: Users can create an account, login and logout.
Dashboard: Users can view all their meal plans and grocery lists.
Meal plan creator: Users can create a new meal plan, edit existing ones, and delete them.
Grocery list creator: Users can generate a grocery list based on the ingredients of a meal plan.
Recipe database: Users can search for recipes and add them to their meal plans.
Export feature: Users can export meal plans and grocery lists as a CSV file.

## Technologies Used
**Flask:** Python based web framework for building web applications.<br />
**wtforms:** A flexible forms validation and rendering library for Python web development.<br />
**PostgreSQL:** A powerful, open source relational database system.<br />
**Hashing:** To covert user passwords to hash before storing them to increase security. </br />
**SQLAlchemy:** A SQL toolkit and ORM that provides a set of high-level API for connecting to databases.<br />
**JavaScript:** A programming language that allows you to add dynamic content to your web pages.

## Installation

### Clone the repository

	$ git clone https://github.com/coderhimanshu1/REMPLR.git
	
### Create a virtual environment and activate it

	$ python3 venv venv
	$ source venv/bin/activate

### Install dependencies

	$ pip install -r requirements.txt
### Create the database

	$ createdb remplr
### Run the application

	$ flask run
O*pen your web browser and go to http://localhost:5000*
## Contributing
Contributions are always welcome! If you have any ideas or suggestions for this project, feel free to submit an issue or a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
