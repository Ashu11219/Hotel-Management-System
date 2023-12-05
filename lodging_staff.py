import csv
import mysql.connector

def connect_to_mysql():
    db_config = {'host': 'localhost',
                 'user': 'root',
                 'password': 'pswrd',
                 'database': 'hotel'}
    return mysql.connector.connect(**db_config)

def details():
    """Displays all records from guest_details.csv"""
    with open("guest_details.csv", mode="r", newline = '\r\n') as file:
        reader = csv.reader(file)
        for record in reader:
            print(record)

def occupancy_status():
    """Displays status of occupancy of all rooms in the hotel"""
    connection = connect_to_mysql()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM occupancy")
    result = cursor.fetchall()
    connection.close()

    for row in result:
        print(row)

def update_occupancy_status(room_number, occupied=True):
    connection = connect_to_mysql()
    cursor = connection.cursor()
    cursor.execute("UPDATE occupancy SET status = %s WHERE room_no = %s",("occupied" if occupied else "not occupied", room_number))
    connection.commit()
    connection.close()

def checkout_guest(guest_name):
    """Checks out a guest by removing record from guest_details.csv and adding it to previous_guests.csv"""
    with open("guest_details.csv", mode="r", newline = '\r\n') as current_file:
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

print("\nWelcome to the Lodging Staff Menu\n")
print('Choose an action:- ')
print("1. View Guest Details")
print("2. View Occupancy Status")
print("3. Checkout Guest")
print("Press any other key to go back to the main menu")

choice = input()

if choice == '1':
    details()
elif choice == '2':
    occupancy_status()
elif choice == '3':
    guest_name = input("Enter the guest's name to checkout: ")
    checkout_guest(guest_name)
else:
    raise Exception('Going back to the main menu.')