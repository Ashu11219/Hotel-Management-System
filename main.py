while True:
    print('Welcome to the Hotel Management System')
    print('We offer the following services:-')
    print('1. Lodging services')
    print('2. Restaurant services')
    choice = int('Which one do you want to avail?: ')

    if choice == 1:
        print('Welcome to the Lodging services')
        print('Press 1 to confirm you are our customer')
        print('Press 2 to confirm you are our staff member')
        print('Press any other number to exit to the main menu')
        choice_lodging = input()

        if choice_lodging == '1':
            loging_customer()
        elif choice_lodging == '2':
            lodging_staff()
        else:
            continue

    elif choice == 2:
        print('Welcome to the Restaurant services')
        print('Press 1 to confirm you are our customer')
        print('Press 2 to confirm you are our staff member')
        print('Press any other number to exit to the main menu')
        choice_restaurant = input()

        if choice_restaurant == '1':
            restaurant_customer()
        elif choice_restaurant == '2':
            restaurant_staff()
        else:
            continue


    else:
        print('Invalid choice')