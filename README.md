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

You can create a waiter account by the help of manager account. Only one waiter should be assigned to each table. So, that he/she won't interfere with other waiters. Waiter is also provided with the information in waiter page that how many tables he can serve.

Waiter can change the menu from menu page, so he/she can show customers only currently available dishes. This also allows waiter to remove and add item in menu. If waiter wants to remove item he/she can simply do it by pressing remove button shown as red cross at the right-top corner of every dish. If waiter wants to add item in menu, he/she is required to add name, price, description (helps customer to understand dish more clearly), ingredients (If someone is allergic then ingredients in a menu are of great help), calories, pictures and type of dish in add-item page.

Waiter can also confirm order by pressing confirm order button in view-orders page, when a table is ready to order. In view-orders page waiter can also prioritize orders by seeing the time they were placed, mark whether the order is on the way, delivered or whether the order is completed, so that the progress of order is tracked correctly. Waiter can also cancel the customer order, so the kitchen staff knows when customers change their mind. Waiter will get notified when the kitchen has prepared the dish, so that he/she can deliver it to the table. Waiter can change the status of an order, so he can keep customer informed about his order. Waiter can also see which tables have received their orders but have yet to pay, so that he/she can prevent people from leaving without paying.

In view-notifications page waiter also gets notified about the table whether order is being prepared or any customer needs help through. Waiter gets notified, if any client needs help so he/she can assist them.![rainbow](/Users/sichen/Downloads/rainbow.png)

### Kitchen Staff

You can create a kitchen staff account by the manager account. 

### Manager

The manager has access to the entire system and can add waiter and kitchen staff accounts. By selecting "add new staff" from the navigation bar, the manager can hire a waiter and a kitchen staff, as well as choose their login and password. Through the "change the menu" page, the manager can remove any food they choose and, if they so choose, add new dishes. Managers can keep an eye on "user id," "table number," "menu items," "order total," "order status," "payment status," and "time placed" by using the "Monitor Orders" feature.
The customer's ID who made the food order is shown in the user id. The tables of the clients are shown by the table number. Each menu item lists the dish or dishes that were ordered as well as the number of dishes that were ordered. Also, it displays the cost of the customer's single selected dish. The Order Total displays the final price based on the number of servings. Order Status indicates whether or not the order bill has been paid. The time and date when the order was placed are displayed under Time Placed. "User id" of the customer is displayed in the monitor notifications, together with "Table Number" and "Message," which inform the management of the order's current status. "Status" indicates whether a waiter is helping the customer or not. 
Manager has the opportunity to revoke notification by selecting "Dismiss" if he so chooses.
View Staff Members displays a staff member's "User Id," which is their user id, "Username", "User Type", which indicates whether they are a waiter or a member of the kitchen staff, "Table Number Range", which indicates the number of tables they have served, and "Actions," which enables the manager to promote a staff member to a customer.
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

