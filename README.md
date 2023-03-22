# Group 26 team project



## Introduction

This team project is an online restaurant system based on flask, which converts most of the in-store restaurant functions to network. Users can log in as customer/waiter/kitchen-staff/manager. It helps to manage the restaurant intuitionisticly and order food easily.

![rainbow](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)



## Authors

- Aleksis Aleksandrs Vilnitis
- Jaskirat Sachdeva
- Youssef Mohamed Helal
- Robert Marshall
- Abdullah Aamir 
- Muhammad Saqib
- Mohamed Mohamed 
- Sicheng Xie

![rainbow](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)
## Setup
Clone this repository to your local machine:

```shell
git clone https://gitlab.cim.rhul.ac.uk/TeamProject26/PROJECT.git
```

Navigate to the root directory of the project:

```shell
cd PROJECT/
```

Install the required packages:

```shell
pip install -r requirements.txt
```

Run the python app:

```shell
python3 main.py
```

![rainbow](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)
## Usage

### Customer
As a customer, you have to sign up for an account to use the restaurant system. When you do, you have the following functionality: 
* See featured items
* View Menu
* Filter menu
* See menu item calories, ingredients
* Add items to cart
* Confirm cart (order)
* Call waiter for help
* Track your orders
* Pay for your order

### Waiter
As a waiter, you have to wait until an admin user creates an account for you and gives you login details. When you're logged in, you have the following functionality:
* View most recent notifications
* View menu
* Edit menu items
* View all orders corresponding to your table range with information about them
* Confirm/Delete orders
* Mark orders as on the way/delivered
* View all notifications corresponding to your table range
* Clear/Dismiss notifications

### Kitchen Staff
As kitchen staff, you have to wait until an admin user creates an account for you and gives you login details. When you're logged in, you have the following functionality:
* View most recent notifications
* View all orders
* Mark orders as preparing/ready
* View all notifications about new orders
* Clear/Dismiss notifications about new orders
* See how long ago an order was placed

### Manager/Admin
There is a single admin/manager account that is created when the app is run. From this account, you have all previously mentioned functionality of both kitchen staff and waiter profiles. Extra functionality includes:
* Add new staff members
* Fire staff members

![rainbow](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)
## Folder Structure

```
PROJECT
├── static
|   ## All Javascripts and CSS codes for styles
|
├── templates
|   ## The moudle templates for all pages
|
├── packages
|   ## Database codes
|
├── instance
|   ## Store the variables for database
|
├── admin
|   ## Codes and templates for administrator
│
├── customer
|   ## Codes and templates for customer
|
├── waiter
|   ## Codes and templates for waiter
|
├── kitchen
|   ## Codes and templates for kitchen staff
|
├── login
|   ## Codes and templates for login function
|
├── sign up
|   ## Codes and templates for sign up function
|
├── requirements.txt
├── Readme.md  
```