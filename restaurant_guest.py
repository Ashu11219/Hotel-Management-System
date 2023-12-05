import csv
import mysql.connector

#funtions:-
def connect_to_mysql():
    db_config = {'host': 'localhost',
                 'user': 'root',
                 'password': 'pswrd',
                 'database': 'hotel'}
    return mysql.connector.connect(**db_config)

def get_price(chosen_dish):
    connection = connect_to_mysql()
    cursor = connection.cursor(dictionary=True)
    result = cursor.execute("SELECT price FROM menu WHERE dish = %s", (chosen_dish,))
    connection.close()

    if result:
        return result.fetchone()['price']
    else:
        return None

def update_total_expense(phone_number, total_price, action):
    with open("guest_details.csv", mode="a", newline = "\r\n") as file:
        reader = csv.reader(file)
        details = list(reader)
        updated_record = []
    # Find the guest by phone number and update the total_expense
    for record in details:
        if record[0] == phone_number:
            if action == 'add':
                global updated_record
                updated_record = str(float(record[3]) + total_price)
                break

            elif action == 'remove':
                global updated_record
                updated_record = str(float(record[3]) - total_price)
                break
    with open("guest_details.csv", mode = "w", newline = "\r\n") as file:
        writer = csv.writer(file)
        writer.writerows(updated_record)

def set_order_status(phone_number, status):
    connection = connect_to_mysql()
    cursor = connection.cursor(dictionary=True)
    result = cursor.execute("UPDATE menu SET status = %s WHERE phone_number = %s", (status, phone_number))
    connection.close()

    if result:
        return result.fetchall()
    else:
        return None

def get_orders_by_phone(phone_number):
    connection = connect_to_mysql()
    cursor = connection.cursor(dictionary=True)
    result = cursor.execute("SELECT dish, status FROM menu WHERE phone_no = %s", (phone_number,))
    connection.close()

    if result:
        return result.fetchall()
    else:
        return None

def insert_feedback(phone_number, feedback):
    connection = connect_to_mysql()
    cursor = connection.cursor()
    cursor.execute("UPDATE guest SET feedback = %s WHERE phone_number = %s", (phone_number, feedback))
    connection.commit()
    connection.close()

#main program:-
print('\nWelcome to the restaurant\n')
print('Choose an action:- ')
print('1. Place an order')
print('2. View your orders')
print('3. Cancel order')
print('4. Submit your valuable feedback')
print('Any other key to exit to main menu')

choice = input()

if choice == '1':
    phone_number = int(input("Enter your phone number: "))
    chosen_dish = input("Enter the dish you want to order: "),
    quantity = int(input("Enter the quantity: "))
    price = get_price(chosen_dish)
    if price:
        total_price = price * quantity
        update_total_expense(phone_number, total_price, 'add')
        set_order_status(phone_number, "processing")
        print("Order placed successfully!")
    else:
        print("Invalid dish. Please choose a valid dish.")
elif choice == '2':
    phone_number = input("Enter your phone number: ")
    orders = get_orders_by_phone(phone_number)

    if orders:
        print('Your orders: ',orders)
    else:
        print('No orders of given phone number found')
elif choice == '3':
    phone_number = int(input("Enter your phone number: "))
    chosen_dish = input("Enter the dish you want to cancel: ")
    quantity = int(input("Enter the quantity to cancel: "))
    price = get_price(chosen_dish)

    if price:
        total_price = price * quantity
        update_total_expense(phone_number, total_price, 'remove')
        set_order_status(phone_number,"cancelled")
        print("Order cancelled successfully!")
    else:
        print("No orders with the entered phone number found.")
elif choice == '4':
    phone_number = input("Enter your phone number: "),
    feedback = input("Enter your valuable feedback: ")
    insert_feedback(phone_number, feedback)
    print("Feedback submitted successfully!")
else:
    raise Exception('Going back to the main menu.')