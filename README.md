# Group 26 team project



## Introduction

**This team project is an online restaurant system based on flask, which converts most of the in-store restaurant functions to network. Users can log in as customer/waiter/kitchen staff/manager. It helps to manage the restaurant intuitionisticly and order food easily.**

![rainbow](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## Setup

The following code can install the required enviroment for running the program. You have to run this code in the project folder by terminal.

```shell
pip install -r requirements.txt
```

![rainbow](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## Usage

### Customer

As a customer, you have to sign up for an account to log into the web. After, you can view the menu to add whatever you like to the cart. Besides, you can filter the menu by the types of dishes if needed and check the ingredients and calories. If you need help, click on the call a waiter button.

### Waiter

You can create a waiter account by the manager account. Waiters can edit the items in the menu by clicking the menu button and check every order by clicking the order button. Orders can be edited or deleted if anything happened to the customer. Notification will be stored on the notification page which will give the table number that needs help. ![rainbow](/Users/sichen/Downloads/rainbow.png

### Kitchen Staff

You can create a kitchen staff account by the manager account. 

### Manager

Manager can view everything in the system and add waiter, kitchen staff account. 

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

