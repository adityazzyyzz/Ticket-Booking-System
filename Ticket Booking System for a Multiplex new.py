class multiplex:
    def __init__(self):
        self.theaters = {
            "Pushpa2": {
                "seats": ["Available"] * 100,
                "showtimes": ["10:00 AM", "2:00 PM", "6:00 PM"],
                "price": 150,
                "bookings": {}  # Format: {showtime: {seat_number: username}}
            },
            "Bhool Bhulaiyaa": {
                "seats": ["Available"] * 120,
                "showtimes": ["11:00 AM", "3:00 PM", "7:00 PM"],
                "price": 200,
                "bookings": {}
            },
            "Shiddat": {
                "seats": ["Available"] * 150,
                "showtimes": ["12:00 PM", "4:00 PM", "8:00 PM"],
                "price": 180,
                "bookings": {}
            }
        }
        self.users = {"admin": "admin123", "user": "user123"}
        self.booked_tickets = []  # Maintain original booked_tickets list
        self.user_bookings = {}  # Additional tracking per user
        self.coupons = {
            "DISCOUNT10": 0.10,
            "SAVE20": 0.20,
        }

    def authenticate(self):
        print("\n--- User Authentication ---")
        for _ in range(3):
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            if username in self.users and self.users[username] == password:
                print("Authentication successful!\n")
                return username
            print("Invalid credentials. Please try again.\n")
        print("Authentication failed. Exiting system.\n")
        return None

    def display_theaters(self):
        print("\n--- Available Theaters and Movies ---")
        for idx, (movie, details) in enumerate(self.theaters.items(), start=1):
            total_seats = len(details['seats'])
            booked_count = sum(len(bookings) for bookings in details.get('bookings', {}).values())
            available_seats = total_seats - booked_count
            
            print(
                f"{idx}. Movie: {movie} | Showtimes: {', '.join(details['showtimes'])} | "
                f"Total Seats: {total_seats} | Available: {available_seats} | "
                f"Price: Rs. {details['price']}"
            )
        print()

    def display_seats(self, movie, showtime):
        print(f"\n--- Seat Layout for {movie} at {showtime} ---")
        seats = self.theaters[movie]["seats"]
        bookings = self.theaters[movie]["bookings"].get(showtime, {})
        
        for i in range(1, len(seats) + 1):
            seat_status = "XX" if i in bookings else f"{i:02}"
            print(f"{seat_status:6}", end=" ")
            if i % 10 == 0:
                print()
        print()

    def book_tickets(self, username):
        print("\n--- Book Tickets ---")
        self.display_theaters()

        try:
            movie_choice = int(input("Select a movie by number: ")) - 1
            movies = list(self.theaters.keys())
            if not (0 <= movie_choice < len(movies)):
                print("Invalid selection. Please try again.\n")
                return
            movie = movies[movie_choice]

            showtimes = self.theaters[movie]["showtimes"]
            print("\nAvailable showtimes:")
            for idx, time in enumerate(showtimes, start=1):
                print(f"{idx}. {time}")
            
            showtime_choice = int(input("Select a showtime by number: ")) - 1
            if not (0 <= showtime_choice < len(showtimes)):
                print("Invalid selection. Please try again.\n")
                return
            showtime = showtimes[showtime_choice]

            self.display_seats(movie, showtime)

            num_tickets = int(input("Enter the number of tickets to book (1-5): "))
            if not (1 <= num_tickets <= 5):
                print("Invalid number of tickets. You can book between 1 and 5 tickets.\n")
                return

            chosen_seats = []
            bookings = self.theaters[movie]["bookings"].get(showtime, {})
            
            for _ in range(num_tickets):
                seat_number = int(input("Enter the seat number you want to book: "))
                if 1 <= seat_number <= len(self.theaters[movie]["seats"]) and seat_number not in bookings:
                    chosen_seats.append(seat_number)
                else:
                    print("Seat not available or invalid. Please try again.\n")
                    return

            # Initialize showtime bookings if not exists
            if showtime not in self.theaters[movie]["bookings"]:
                self.theaters[movie]["bookings"][showtime] = {}

            # Apply coupon if provided
            coupon_code = input("Enter coupon code (DISCOUNT10 / SAVE20) or press Enter to skip: ").strip()
            if coupon_code in self.coupons:
                discount = self.coupons[coupon_code]
                discount_amount = self.theaters[movie]["price"] * discount
                self.theaters[movie]["price"] -= discount_amount
                print(f"Coupon applied! You saved Rs. {discount_amount}")
            else:
                print("Invalid coupon code or format. Please enter a valid uppercase coupon code.")

            # Update theater bookings
            for seat in chosen_seats:
                self.theaters[movie]["bookings"][showtime][seat] = username
                self.theaters[movie]["seats"][seat - 1] = "Booked"  # Update original seats array
            
            # Update booked_tickets list 
            self.booked_tickets.append({
                "movie": movie,
                "showtime": showtime,
                "seats": chosen_seats,
                "price": self.theaters[movie]["price"],
                "username": username
            })
            
            # Update user_bookings (new tracking)
            if username not in self.user_bookings:
                self.user_bookings[username] = []
            self.user_bookings[username].append({
                "movie": movie,
                "showtime": showtime,
                "seats": chosen_seats,
                "price": self.theaters[movie]["price"]
            })
            
            # Check for free popcorn reward
            if len(chosen_seats) == 5:
                print("Congratulations! You've booked 5 tickets and earned a free popcorn voucher!")
            
            print(f"\nSuccessfully booked seats: {chosen_seats} for {movie} at {showtime}")
            print(f"Total price: Rs. {self.theaters[movie]['price']}\n")


        except ValueError:
            print("Invalid input. Please enter valid numbers.\n")
            
    def view_bookings(self, username):
        user_tickets = [ticket for ticket in self.booked_tickets if ticket["username"] == username]
        
        if not user_tickets:
            print("\nNo tickets booked yet.\n")
            return

        print("\n--- Your Booked Tickets ---")
        for idx, ticket in enumerate(user_tickets, start=1):
            print(f"{idx}. Movie: {ticket['movie']}")
            print(f"   Showtime: {ticket['showtime']}")
            print(f"   Seats: {ticket['seats']}")
            print(f"   Price: Rs. {ticket['price']}")
            print("   " + "-" * 40)

    def cancel_ticket(self, username):
            user_tickets = [ticket for ticket in self.booked_tickets if ticket["username"] == username]
            
            if not user_tickets:
                print("\nNo tickets booked yet.\n")
                return
            print("\n--- Your Booked Tickets ---")
            print("Note: Only 50% refund will be given on cancellation\n")
            for idx, ticket in enumerate(user_tickets, start=1):
                print(f"{idx}. Movie: {ticket['movie']} | Showtime: {ticket['showtime']} | "
                      f"Seats: {ticket['seats']} | Price: Rs. {ticket['price']}")
    
            try:
                ticket_choice = int(input("\nEnter the ticket number to cancel: ")) - 1
                if not (0 <= ticket_choice < len(user_tickets)):
                    print("Invalid ticket selection.\n")
                    return
                ticket = user_tickets[ticket_choice]
                print(f"\nSeats booked for {ticket['movie']} at {ticket['showtime']}: {ticket['seats']}")
                
                print("\nEnter seat numbers to cancel (comma-separated):")
                seat_input = input("Example - for seats 1,2,3 enter: 1,2,3\n").strip()
                seats_to_cancel = [int(s.strip()) for s in seat_input.split(',')]

                # Validate all seats before canceling
                if not all(seat in ticket['seats'] for seat in seats_to_cancel):
                    print("One or more selected seats are not valid for this booking.\n")
                    return

                total_refund = 0
                for seat in seats_to_cancel:
                    # Calculate refund amount (50% of single seat price)
                    single_seat_price = self.theaters[ticket['movie']]['price']
                    refund_amount = round(single_seat_price * 0.50)  # 50% refund
                    total_refund += refund_amount
                    
                    # Update theater bookings
                    del self.theaters[ticket['movie']]["bookings"][ticket['showtime']][seat]
                    self.theaters[ticket['movie']]["seats"][seat - 1] = "Available"

                    # Update booked_tickets list and price
                    ticket['seats'].remove(seat)
                    ticket['price'] -= single_seat_price  # Reduce total price
                    if not ticket['seats']:
                        self.booked_tickets.remove(ticket)

                    # Update user_bookings
                    if username in self.user_bookings:
                        for booking in self.user_bookings[username]:
                            if (booking['movie'] == ticket['movie'] and 
                                booking['showtime'] == ticket['showtime'] and 
                                seat in booking['seats']):
                                booking['seats'].remove(seat)
                                booking['price'] -= single_seat_price  # Reduce total price
                                if not booking['seats']:
                                    self.user_bookings[username].remove(booking)
                
                print(f"\nSuccessfully canceled seats: {seats_to_cancel}")
                print(f"Total refund amount (50%): Rs. {total_refund}")
            except ValueError:
                print("Invalid input. Please enter valid numbers.\n")
                
    def admin_book_tickets(self):
        print("\n--- Admin Book Tickets ---")
        print("Note: Maximum 20 seats can be booked at once\n")
        self.display_theaters()

        try:
            movie_choice = int(input("Select a movie by number: ")) - 1
            movies = list(self.theaters.keys())
            if not (0 <= movie_choice < len(movies)):
                print("Invalid selection. Please try again.\n")
                return
            movie = movies[movie_choice]

            showtimes = self.theaters[movie]["showtimes"]
            print("\nAvailable showtimes:")
            for idx, time in enumerate(showtimes, start=1):
                print(f"{idx}. {time}")
            
            showtime_choice = int(input("Select a showtime by number: ")) - 1
            if not (0 <= showtime_choice < len(showtimes)):
                print("Invalid selection. Please try again.\n")
                return
            showtime = showtimes[showtime_choice]

            self.display_seats(movie, showtime)

            num_tickets = int(input("Enter the number of tickets to book (1-20): "))
            if not (1 <= num_tickets <= 20):
                print("Invalid number of tickets. Admin can book between 1 and 20 tickets.\n")
                return

            chosen_seats = []
            bookings = self.theaters[movie]["bookings"].get(showtime, {})
            
            print("\nEnter seat numbers (comma-separated) to book:")
            seat_input = input("Example - for seats 1,2,3 enter: 1,2,3\n").strip()
            selected_seats = [int(s.strip()) for s in seat_input.split(',')]

            if len(selected_seats) != num_tickets:
                print("Number of seats selected doesn't match the number of tickets specified.\n")
                return

            if len(selected_seats) > 20:
                print("Cannot book more than 20 seats at once.\n")
                return

            # Validate all seats
            for seat_number in selected_seats:
                if 1 <= seat_number <= len(self.theaters[movie]["seats"]) and seat_number not in bookings:
                    chosen_seats.append(seat_number)
                else:
                    print(f"Seat {seat_number} is not available or invalid.\n")
                    return

            # Initialize showtime bookings if not exists
            if showtime not in self.theaters[movie]["bookings"]:
                self.theaters[movie]["bookings"][showtime] = {}

            # Update bookings
            total_price = 0
            for seat in chosen_seats:
                self.theaters[movie]["bookings"][showtime][seat] = "admin"
                self.theaters[movie]["seats"][seat - 1] = "Booked"
                total_price += self.theaters[movie]["price"]

            # Update booked_tickets list
            self.booked_tickets.append({
                "movie": movie,
                "showtime": showtime,
                "seats": chosen_seats,
                "price": total_price,
                "username": "admin"
            })

            print(f"\nSuccessfully booked seats: {chosen_seats} for {movie} at {showtime}")
            print(f"Total amount: Rs. {total_price}\n")

        except ValueError as e:
            print("Invalid input. Please enter valid numbers.\n")

    def admin_cancel_tickets(self):
        admin_tickets = [ticket for ticket in self.booked_tickets if ticket["username"] == "admin"]
        
        if not admin_tickets:
            print("\nNo tickets booked by admin.\n")
            return

        print("\n--- Admin Cancel Tickets ---")
        print("Note: Maximum 20 seats can be canceled at once\n")
        
        for idx, ticket in enumerate(admin_tickets, start=1):
            print(f"{idx}. Movie: {ticket['movie']} | Showtime: {ticket['showtime']} | "
                  f"Seats: {ticket['seats']} | Price: Rs. {ticket['price']}")

        try:
            ticket_choice = int(input("\nEnter the ticket number to cancel from: ")) - 1
            if not (0 <= ticket_choice < len(admin_tickets)):
                print("Invalid ticket selection.\n")
                return

            ticket = admin_tickets[ticket_choice]
            print(f"\nCurrently booked seats for {ticket['movie']} at {ticket['showtime']}: {ticket['seats']}")
            
            print("\nEnter seat numbers to cancel (comma-separated):")
            seat_input = input("Example - for seats 1,2,3 enter: 1,2,3\n").strip()
            seats_to_cancel = [int(s.strip()) for s in seat_input.split(',')]

            if len(seats_to_cancel) > 20:
                print("Cannot cancel more than 20 seats at once.\n")
                return

            # Validate all seats before canceling
            if not all(seat in ticket['seats'] for seat in seats_to_cancel):
                print("One or more selected seats are not valid for this booking.\n")
                return

            total_refund = 0
            for seat in seats_to_cancel:
                # Update theater bookings
                del self.theaters[ticket['movie']]["bookings"][ticket['showtime']][seat]
                self.theaters[ticket['movie']]["seats"][seat - 1] = "Available"
                total_refund += self.theaters[ticket['movie']]['price']

                # Update ticket seats
                ticket['seats'].remove(seat)

            # Update ticket price
            ticket['price'] -= total_refund

            # Remove ticket if no seats left
            if not ticket['seats']:
                self.booked_tickets.remove(ticket)

            print(f"\nSuccessfully canceled seats: {seats_to_cancel}")
            print(f"Total amount to be refunded: Rs. {total_refund}\n")

        except ValueError:
            print("Invalid input. Please enter valid numbers.\n")

    def admin_cancel_user_tickets(self):
        print("\n--- Admin Cancel User Tickets ---")
        if not self.booked_tickets:
            print("No tickets booked by users.\n")
            return

        print("\n--- All User Bookings ---")
        for idx, ticket in enumerate(self.booked_tickets, start=1):
            print(f"{idx}. Movie: {ticket['movie']} | Showtime: {ticket['showtime']} | "
                  f"Seats: {ticket['seats']} | Price: Rs. {ticket['price']} | Booked by: {ticket['username']}")

        try:
            ticket_choice = int(input("\nEnter the ticket number to cancel: ")) - 1
            if not (0 <= ticket_choice < len(self.booked_tickets)):
                print("Invalid ticket selection.\n")
                return

            ticket = self.booked_tickets[ticket_choice]
            print(f"\nCurrently booked seats for {ticket['movie']} at {ticket['showtime']}: {ticket['seats']}")
            
            print("\nEnter seat numbers to cancel (comma-separated):")
            seat_input = input("Example - for seats 1,2,3 enter: 1,2,3\n").strip()
            seats_to_cancel = [int(s.strip()) for s in seat_input.split(',')]

            # Validate all seats before canceling
            if not all(seat in ticket['seats'] for seat in seats_to_cancel):
                print("One or more selected seats are not valid for this booking.\n")
                return

            total_refund = 0
            for seat in seats_to_cancel:
                # Update theater bookings
                del self.theaters[ticket['movie']]["bookings"][ticket['showtime']][seat]
                self.theaters[ticket['movie']]["seats"][seat - 1] = "Available"
                total_refund += self.theaters[ticket['movie']]['price']

                # Update ticket seats
                ticket['seats'].remove(seat)

            # Update ticket price
            ticket['price'] -= total_refund

            # Remove ticket if no seats left
            if not ticket['seats']:
                self.booked_tickets.remove(ticket)

            print(f"\nSuccessfully canceled seats: {seats_to_cancel}")
            print(f"Total amount to be refunded: Rs. {total_refund}\n")

        except ValueError:
            print("Invalid input. Please enter valid numbers.\n")

    def admin_panel(self):
        while True:
            print("\n--- Admin Panel ---")
            print("1. View Theater Details")
            print("2. Reset Seat Availability")
            print("3. Change Ticket Prices")
            print("4. Modify Seat Count")
            print("5. Book Seats (Max 20)")
            print("6. Cancel Seats (Max 20)")
            print("7. View All Bookings")
            print("8. Cancel User Tickets")
            print("9. Exit Admin Panel")

            try:
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    self.display_theaters()
                    for movie, details in self.theaters.items():
                        print(f"\nMovie: {movie}")
                        for showtime in details['showtimes']:
                            booked = len(details.get('bookings', {}).get(showtime, {}))
                            available = len(details['seats']) - booked
                            print(f"Showtime: {showtime}")
                            print(f"Booked Seats: {booked}")
                            print(f"Available Seats: {available}")
                        print("-" * 40)
                elif choice == 2:
                    self.display_theaters()
                    try:
                        movie_choice = int(input("Select a movie to reset seats by number: ")) - 1
                        movies = list(self.theaters.keys())
                        if 0 <= movie_choice < len(movies):
                            movie = movies[movie_choice]
                            self.theaters[movie]["seats"] = ["Available"] * len(self.theaters[movie]["seats"])
                            self.theaters[movie]["bookings"] = {}
                            self.booked_tickets = [t for t in self.booked_tickets if t["movie"] != movie]
                            print(f"All seats for {movie} have been reset.\n")
                        else:
                            print("Invalid selection.\n")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.\n")
                elif choice == 3:
                    self.display_theaters()
                    try:
                        movie_choice = int(input("Select a movie to change price for by number: ")) - 1
                        movies = list(self.theaters.keys())
                        if 0 <= movie_choice < len(movies):
                            movie = movies[movie_choice]
                            new_price = int(input("Enter new price: "))
                            if new_price > 0:
                                self.theaters[movie]["price"] = new_price
                                print(f"Price updated for {movie} to Rs. {new_price}\n")
                            else:
                                print("Invalid price.\n")
                        else:
                            print("Invalid selection.\n")
                    except ValueError:
                        print("Invalid input. Please enter valid numbers.\n")
                elif choice == 4:
                    self.display_theaters()
                    try:
                        movie_choice = int(input("Select a movie to modify seats for by number: ")) - 1
                        movies = list(self.theaters.keys())
                        if 0 <= movie_choice < len(movies):
                            movie = movies[movie_choice]
                            current_seats = len(self.theaters[movie]["seats"])
                            print(f"Current seat count: {current_seats}")
                            new_count = int(input("Enter new seat count (max 100): "))
                            if 0 < new_count <= 100:
                                if new_count > current_seats:
                                    self.theaters[movie]["seats"].extend(["Available"] * (new_count - current_seats))
                                else:
                                    self.theaters[movie]["seats"] = self.theaters[movie]["seats"][:new_count]
                                print(f"Seat count updated to {new_count}\n")
                            else:
                                print("Invalid seat count.\n")
                        else:
                            print("Invalid selection.\n")
                    except ValueError:
                        print("Invalid input. Please enter valid numbers.\n")
                elif choice == 5:
                    self.admin_book_tickets()
                elif choice == 6:
                    self.admin_cancel_tickets()
                elif choice == 7:
                    print("\n--- All Bookings ---")
                    if not self.booked_tickets:
                        print("No tickets booked yet.\n")
                    else:
                        for ticket in self.booked_tickets:
                            print(f"Movie: {ticket['movie']}")
                            print(f"Showtime: {ticket['showtime']}")
                            print(f"Seats: {ticket['seats']}")
                            print(f"Price: Rs. {ticket['price']}")
                            print(f"Booked by: {ticket['username']}")
                            print("-" * 40)
                elif choice == 8:
                    self.admin_cancel_user_tickets()
                elif choice == 9:
                    print("Exiting Admin Panel.\n")
                    break
                else:
                    print("Invalid choice. Please try again.\n")
            except ValueError:
                print("Invalid input. Please enter a number.\n")

    def user_panel(self, username):
        while True:
            print("\n--- User Panel ---")
            print("1. View Available Shows")
            print("2. Book Tickets")
            print("3. View My Bookings")
            print("4. Cancel Ticket")
            print("5. Exit User Panel")

            try:
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    self.display_theaters()
                elif choice == 2:
                    self.book_tickets(username)
                elif choice == 3:
                    self.view_bookings(username)
                elif choice == 4:
                    self.cancel_ticket(username)
                elif choice == 5:
                    print("\nExiting User Panel.\n")
                    break
                else:
                    print("Invalid choice. Please try again.\n")
            except ValueError:
                print("Invalid input. Please enter a number.\n")

    def run(self):
        while True:
            print("\n--- Multiplex Ticketing System ---")
            print("1. Admin Login")
            print("2. User Login")
            print("3. Exit")

            try:
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    username = self.authenticate()
                    if username == "admin":
                        self.admin_panel()
                elif choice == 2:
                    username = self.authenticate()
                    if username:
                        self.user_panel(username)
                elif choice == 3:
                    print("Thank you for using the Multiplex Ticketing System. Goodbye!\n")
                    break
                else:
                    print("Invalid choice. Please try again.\n")
            except ValueError:
                print("Invalid input. Please enter a number.\n")

if __name__ == "__main__":
    multiplex = multiplex()
    multiplex.run()