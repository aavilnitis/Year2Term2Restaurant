from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from packages.models import MenuItem, Order, User, db
from admin.static.functions.admin_functions import populate_menu, check_cleared_notifs, admin_required, add_item, add_staff

# register customer_view as a Flask Blueprint
admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")
    
# HOME ROUTE
@admin.route('/')
@admin_required
def home():
    """Queries database for all non-cleared type notifications and renders Admin home page
        template that displays said notifications

    Returns:
        str: The HTML content of the admin-home template
    """
    notifications = check_cleared_notifs()
    if len(notifications) > 0:
        return render_template('admin-home.html', notifications = notifications)
    else:
        return render_template('admin-home.html')
    
# NOTIFICATIONS
@admin.route('view-notifications')
@admin_required
def viewNotifications():
    """Queries the database for all notifications and renders the admin-view-notifications 
        template displaying all notifications with an option to dismiss them.

    Returns:
        str: The HTML content of the admin-view-notifications template.
    """
    notifications = check_cleared_notifs()
    return render_template('admin-view-notifications.html', notifications = notifications)

@admin.route('/remove-notification-page/<int:notif_id>', methods = ['POST'])
@admin_required
def removeNotificationPage(notif_id):
    """Removes a notification from admin notifications page by adding it to cleared_notifs array.
        It doesn't remove notification by deleting it like in other views as other staff
        members might still need that notification.

    Args:
        notif_id (id): The id of the Notification to remove

    Returns:
        flask.Response: A redirect response to the kitchen staff notifications page
    """
    cleared_notifs = session['cleared_notifs']
    cleared_notifs.append(notif_id)
    session['cleared_notifs'] = cleared_notifs
    return redirect(url_for('admin.viewNotifications'))

@admin.route('/remove-notification/<int:notif_id>', methods = ['POST'])
@admin_required
def removeNotification(notif_id):
    """Removes a notification from admin home page by adding it to cleared_notifs array.
        It doesn't remove notification by deleting it like in other views as other staff
        members might still need that notification.

    Args:
        notif_id (id): The id of the Notification to remove

    Returns:
        flask.Response: A redirect response to the kitchen staff home page
    """
    cleared_notifs = session['cleared_notifs']
    cleared_notifs.append(notif_id)
    session['cleared_notifs'] = cleared_notifs
    return redirect(url_for('admin.home'))

    
# ORDERS
@admin.route('view-orders')
@admin_required
def viewOrders():
    """Queries the database for all orders and renders the admin-view-orders template 
        displaying all orders.

    Returns:
        str: The HTML content of the admin-view-order template.
    """
    orders = Order.query.all()
    menu_items = MenuItem.query.all()
    users = User.query.all()
    return render_template('admin-view-order.html', orders = orders, menu_items = menu_items, users = users)


# MENU 
@admin.route('/menu')
@admin_required
def menu():
    """Checks if a MenuItem exists, if not it will call the populate_menu function to update menu data

    Returns:
        str: The HTML content for the menu page template with all MenuItems
    """
    if MenuItem.query.first() == None:
        populate_menu()
    menu_items = MenuItem.query.all()
    return render_template('admin-menu.html', menu_items=menu_items)



@admin.route('/admin-add-item', methods=['GET', 'POST'])
@admin_required
def addItem():
    """Renders the add-item page and calls function for adding a new MenuItem to database

    Returns:
        str: The HTML content for for the admin-add-item page, or if form is submitted taken back to menu page
    """
    if request.method == 'POST':
        add_item()
        return redirect(url_for('admin.menu'))
    types = db.session.query(MenuItem.type).distinct()
    return render_template('admin-add_item.html', types = types)

@admin.route('/remove-item/<int:item_id>', methods = ['GET','POST'])
@admin_required
def removeItem(item_id):
    """Gets MenuItem using item_id and removes it from database

    Args:
        item_id (int): The id of the MenuItem to be removed

    Returns:
        flask.Response: Redirects admin back to menu
    """
    item = MenuItem.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit() 
    return redirect(url_for('admin.menu'))

@admin.route('/edit-item/<int:item_id>', methods = ['GET','POST'])
@admin_required
def editItem(item_id):
    """Edits data of an existing MenuItem

    Args:
        item_id (id): The id of the MenuItem in database

    Returns:
        str: The HTML content for menu page after editing a MenuItem, or renders the edit-item page to allow admin to edit item
    """
    item = MenuItem.query.get(item_id)
    if item:
        if request.method == 'POST':
            add_item()
            return redirect(url_for('admin.menu'))
        else:
            types = db.session.query(MenuItem.type).distinct()
            ingredient_save = ""
            for ingredient in item.ingredients:
                ingredient_save = ingredient_save + "," + ingredient.name
            return render_template('admin-edit_item.html', types = types, item = item, ingredient_save = ingredient_save[1:])
    else:
        flash("Something went wrong!", category = "error")
        return redirect(url_for('admin.menu'))


# ADD WAITER/KITCHEN
@admin.route('add-new-staff', methods=['GET', 'POST'])
@admin_required
def addNewStaff():
    if request.method == 'POST':
        add_staff()
        return redirect(url_for('admin.home'))
            
    return render_template('add-new-staff.html')


@admin.route('view-staff', methods = ['GET', 'POST'])
@admin_required
def viewStaff():
    users = User.query.filter(User.user_type.in_(['waiter', 'kitchen_staff'])).all()
    return render_template('admin-view-staff.html', users = users)

@admin.route('fire-staff/<int:staff_id>', methods = ['GET', 'POST'])
@admin_required
def fireStaff(staff_id):
    user = User.query.get(staff_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.viewStaff'))