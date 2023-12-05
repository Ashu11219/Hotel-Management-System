import csv
import mysql.connector

#functions:-
def connect_to_mysql():
    db_config = {'host': 'localhost',
                 'user': 'root',
                 'password': 'pswrd',
                 'database': 'hotel'}
    return mysql.connector.connect(**db_config)

def get_empty_room_number():
    connection = connect_to_mysql()
    cursor = connection.cursor()
    cursor.execute("SELECT room_no FROM occupancy WHERE status = 'not occupied' LIMIT 1")
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else None

def update_occupancy_status(room_number, occupied=True):
    connection = connect_to_mysql()
    cursor = connection.cursor()

    cursor.execute("UPDATE occupancy SET status = %s WHERE room_no = %s",("occupied" if occupied else "not occupied", room_number))

    connection.commit()
    connection.close()

#main program:-
print('Welcome to our hotel')
print('Choose an action:- ')
print('1. Book a room')
print('Any other key to exit to main menu')
choice = input()

if choice == '1':
    guest_name = input("Enter your name: ")
    guest_number = int(input('Enter your phone number: '))
    room_number = get_empty_room_number() # Get an empty room number using the function

    # Check if a room is available
    if room_number is not None:
        total_expense = 0.0
        update_occupancy_status(room_number)

        # Prepare data
        guest_data = [guest_name, guest_number, room_number, total_expense]

        # Append data to the CSV file
        with open("guest_details.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(guest_data)

        print("Check-in successful, enjoy your stay in room", room_number)
    else:
        print("Sorry, the hotel is fully occupied, no rooms available.")

else:
    raise Exception('Going back to the main menu.')