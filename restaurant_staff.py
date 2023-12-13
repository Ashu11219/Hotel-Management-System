import csv
import mysql.connector

#functions:-
def connect_to_mysql():
    db_config = {'host': 'localhost',
                 'user': 'root',
                 'password': 'pswrd',
                 'database': 'hotel'}
    return mysql.connector.connect(**db_config)

#main program:-
def restaurant_staff():
    print('\nWelcome to the Restaurant Staff Menu\n')
    print('Choose an action:- ')
    print('1. View Orders')
    print('2. View Customer details')
    print('3. View Feedbacks')
    print("Press any other key to go back to the main menu")

    choice = input()

    if choice == '1':
        connection = connect_to_mysql()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT phone_number, chosen_dish, quantity, status FROM guest_orders")
        orders = cursor.fetchall()
        connection.close()

        if orders:
            print("Orders:")
            for order in orders:
                print(order)
        else:
            print("No orders found.")
    elif choice == '2':
        with open("guest_details.csv", mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                print(row)
    elif choice == '3':
        connection = connect_to_mysql()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT phone_number, feedback FROM guest_orders")
        orders = cursor.fetchall()
        connection.close()

        if orders:
            print("Orders:")
            for order in orders:
                print(order)
        else:
            print("No orders found.")
    else:
        raise Exception('Going back to the main menu.')