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
    """Searches for an empty room to be allotted to the customer checking in"""
    connection = connect_to_mysql()
    cursor = connection.cursor()
    cursor.execute("SELECT room_no FROM occupancy WHERE status = 'not occupied' LIMIT 1") #occupancy is a table name in hotel database
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else None

def update_occupancy_status(room_number, occupied=True):
    """Updates the occupancy status in occupancy table"""
    connection = connect_to_mysql()
    cursor = connection.cursor()
    cursor.execute("UPDATE occupancy SET status = %s WHERE room_no = %s",("occupied" if occupied else "not occupied", room_number)) #occupancy is a table name in hotel database
    connection.commit()
    connection.close()

def checkout_guest(guest_name):
    """Checks out a guest by removing record from guest_details.csv and adding it to previous_guests.csv"""
    with open("guest_details.csv", mode="r", newline = "\r\n") as current_file:
        reader = csv.reader(current_file)
        details = list(reader)
        new_details = []
        checked_out_guest = []
        # Find the guest by name
        for record in details:
            if record[0] == guest_name:
                checked_out_guest = record
            else:
                new_details.append(record)

    # Write the updated data back to guest_details.csv (without the checked-out guest)
    with open("guest_details.csv", mode="w", newline="") as current_file:
        writer = csv.writer(current_file)
        writer.writerows(new_details)

    with open("previous_guests.csv", mode="a", newline="") as prev_file:
        prev_writer = csv.writer(prev_file)
        prev_writer.writerow(checked_out_guest)

    print(guest_name,' has been checked out.')

    # Update the occupancy status to mark the room as not occupied
    update_occupancy_status(int(checked_out_guest[1]), occupied=False)

#main program:-
print('\nWelcome to our hotel\n')
print('Choose an action:- ')
print('1. Book a room')
print('2. Checkout')
print('Any other key to exit to main menu')

choice = input()

if choice == '1':
    guest_name = input("Enter your name: ")
    guest_number = int(input('Enter your phone number: '))
    room_number = get_empty_room_number() # Attempt to get an empty room number using the function

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
elif choice == '2':
    guest_name = input("Enter your name to checkout: ")
    checkout_guest(guest_name)
else:
    raise Exception('Going back to the main menu.')