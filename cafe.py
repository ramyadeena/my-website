from customer_data import CustomerData
from menus import (tea_list, coffee_list, books_list, smoothies_list)

class CaffeineCloud:
    def __init__(self):
        # set the initial menus from the menus file
        self.tea = tea_list
        self.coffee = coffee_list
        self.books = books_list
        self.smoothies = smoothies_list

        self.order = []
        self.total = 0.0
        self.customer_data = CustomerData()

    def print_menu(self, heading, menu):            
        print(f"\n{heading}:")
        if menu is self.books:  # for books, we print more than just the price
            for book, info in menu.items():
                print(f"{book}: £{info["price"]:.2f}")
                print(f"\tby {info["author"]}")
                print(f"\tGenre: {info["genre"]}")
        else:
            for item, price in menu.items():
                print(f"{item}: £{price:.2f}")

    def purchase_from_menu(self, heading, menu):
        self.print_menu(heading, menu)
        pick = input("\nPlease enter your chosen items below (if multiple, please separate items by ','): ")
        if pick.strip() == "":
            return
        items = [item.strip().title() for item in pick.split(",")]
        for item in items:
            if item in menu:
                if menu is self.books:  # for books, we get the price from each book's dictionary
                    price = menu[item]["price"]
                else:  # for everything else, the price is directly in the menu dictionary
                    price = menu[item]
                self.order.append((item, price))
                self.total += price
                print(f"\nThe following items have been added: {item}")
                print(f"Your current total is: £{self.total:.2f}")
            else:
                print(f"\nItem cannot be found: {item}")

    def ask_delivery_details(self):
        deliver = input("\nYour order includes books. Would you like them delivered (yes or no)? ").lower()
        if deliver == "yes" or deliver == "y":
            name = input("Enter your name: ")
            name_and_address = name
            n = 1
            print("Enter each line of your address, or leave the line blank to finish.")
            while True:
                address_line = input(f"Line {n}: ").strip()
                if address_line == "":
                    break
                else:
                    name_and_address += f"\n{address_line}"
                    n += 1
            print("\nOkay! We'll deliver your books to:")
            print(name_and_address)
            self.customer_data.add_delivery(name_and_address)
        else:
            return

    def checkout(self):
        print("\nYour current order:")
        ordered_books = False
        for item, price in self.order:
            print(f"{item}, £{price:.2f}")
            if item in self.tea:
                item_type = "tea"
            elif item in self.coffee:
                item_type = "coffee"
            elif item in self.smoothies:
                item_type = "smoothie"
            else:  # we don't add items to self.order that aren't in one of the menus, so anything else is a book
                item_type = "book"
                ordered_books = True
            self.customer_data.add_purchase(item, item_type, price)
        print(f"\nTotal: £{self.total:.2f}")
        if ordered_books:
            self.ask_delivery_details()
        print("\nThank you for shopping at Caffeine Cloud!")
        # Move to next customer number, and reset the total and ordereditems
        self.customer_data.next_customer()
        self.total = 0.0
        self.order = []

    def print_purchase_history(self):
        for customer_number in self.customer_data.get_customers():
            purchases = self.customer_data.get_customer_purchases(customer_number)
            num_purchases = len(purchases)

            print(f"\nCustomer #{customer_number} has {num_purchases} purchases:")
            for purchase in purchases:
                print(f"- {purchase['name']}: £{purchase['price']:.2f}")

            customer_total = self.customer_data.get_customer_total_spend(customer_number)
            print(f"Their total was £{customer_total:.2f}")

    def print_deliveries(self):
        for customer_number in self.customer_data.get_customers():
            if not self.customer_data.has_delivery(customer_number):
                continue

            books = self.customer_data.get_customer_purchases(customer_number, "book")

            print(f"\nCustomer #{customer_number} bought these books:")
            for book in books:
                print(f"- {book['name']}")

            print("They would like them delivered to:")
            print(self.customer_data.get_address(customer_number))

    def staff_menu(self):
        while True:
            print("\nWhat do you want to do?")
            print("1. Show purchase history")
            print("2. Show deliveries")
            print("3. Back to customer options")
            pick = input("Please select an option: ").strip()

            if pick == "1":
                self.print_purchase_history()
            elif pick == "2":
                self.print_deliveries()
            elif pick == "3":
                break
            else:
                print("Invalid choice. Please try again.")

    def start(self):
        print("Welcome to Caffeine Cloud!!")
        print("What can I get you?")

        while True:
            print("\n1. Buy teas/coffees")
            print("2. Buy smoothies")
            print("3. Buy books")
            print("4. Checkout")
            print("5. Staff options")
            print("6. Exit")
            pick = input("Please select an option: ").strip()

            if pick == "1":
                self.purchase_from_menu("Tea & Coffee menu", self.tea | self.coffee)
            elif pick == "2":
                self.purchase_from_menu("Smoothie menu", self.smoothies)
            elif pick == "3":
                self.purchase_from_menu("Our current book selection", self.books)
            elif pick == "4":
                self.checkout()
                print(f"\nNow serving customer #{self.customer_data.current_customer}.")
            elif pick == "5":
                employee_pass = input("Enter staff password: ")
                if employee_pass == "C0FF33":
                    self.staff_menu()
                else:
                    print("\nInvalid password. Staff option access denied.")
            elif pick == "6":
                print("\nGoodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    store = CaffeineCloud()
    store.start()
