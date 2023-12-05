import csv
import mysql.connector

#functions:-
def connect_to_mysql():
    db_config = {'host': 'localhost',
                 'user': 'root',
                 'password': 'pswrd',
                 'database': 'hotel'}
    return mysql.connector.connect(**db_config)

def details():
    """Displays all records from guest_details.csv"""
    with open("guest_details.csv", mode="r", newline = "\r\n") as file:
        reader = csv.reader(file)
        for record in reader:
            print(record)

def occupancy_status():
    """Displays status of occupancy of all rooms in the hotel"""
    connection = connect_to_mysql()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM occupancy") #occupancy is a table name in hotel database
    result = cursor.fetchall()
    connection.close()

    for row in result:
        print(row)


#main program:-
print('\nWelcome to the Lodging Staff Menu\n')
print('Choose an action:- ')
print('1. View Guest Details')
print('2. View Occupancy Status')
print("Press any other key to go back to the main menu")

choice = input()

if choice == '1':
    details()
elif choice == '2':
    occupancy_status()
else:
    raise Exception('Going back to the main menu.')