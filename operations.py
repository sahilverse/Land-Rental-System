from datetime import datetime
from write import create_rental_receipt, create_return_receipt, update_availability_in_file, add_rented_land_to_file

now = datetime.now()

# This Module contains the functions to perform operations on the data.


invoice_count = 0
return_invoice_count = 0


# generate the rental invoice for the rented land.
def generate_rental_invoice(kitta_number, customer_name, duration, area, city, direction, price, rented_lands: list[dict]):
    global invoice_count

    total = price * duration

    total_amount_for_customer = 0
    invoice_number = None

    for rented_land in rented_lands:
        if rented_land['customer_name'].lower() == customer_name.lower():
            invoice_number = rented_land['invoice_number']
            total_amount_for_customer += rented_land['total_price']
            break

    if invoice_number is None:
        invoice_count += 1
        invoice_number = invoice_count

    total += total_amount_for_customer

    create_rental_receipt(invoice_number, kitta_number, customer_name,
                          duration, area, city, direction, price, total)
    return invoice_number


# Generate the return invoice for the rented land.
def generate_return_invoice(kitta_number, customer_name, duration, extra_duration, area, city, direction, price, fine):
    global return_invoice_count
    return_invoice_count += 1
    return_invoice_number = return_invoice_count
    create_return_receipt(return_invoice_number, kitta_number, customer_name,
                          duration, extra_duration, area, city, direction, price, fine)

    return return_invoice_number, return_invoice_count

# calculate the duration of the rented land.


def calculate_duration(rental_date):

    return_date = now.date().strftime('%d-%m-%Y')
    return_date = datetime.strptime(return_date, '%d-%m-%Y')
    rental_date = datetime.strptime(rental_date, '%d-%m-%Y')

    duration = (return_date - rental_date).days
    duration_in_months = duration / 30

    return duration_in_months

#  Calculate the fine for the extra duration of the rented land.


def calculate_fine(land, duration_of_rent):

    extra_duration = duration_of_rent - land["duration"]
    fine = extra_duration * 500
    return extra_duration, fine


# Handle the return of the rented land.
def handle_return_scenarios(kitta_number, land: list[dict], duration_of_rent, lands_data: list[dict], rented_lands: list[dict]):
    if duration_of_rent > land['duration']:
        print("Do you have renewed contract? (y/n): ")
        is_return = input()
        if is_return.lower() == 'y':
            print("Land is Returned Successfully. No Fine is Charged.")
            rented_lands.remove(land)
            for land in lands_data:
                if land['kitta_number'] == kitta_number:
                    land['availability'] = "Available"
            update_availability_in_file(lands_data)
        elif is_return.lower() == 'n':
            extra_duration, fine = calculate_fine(land, duration_of_rent)
            generate_return_invoice(land["kitta_number"], land["customer_name"], land['duration'], extra_duration, land["area"],
                                    land["location"], land["direction"], land["price"], fine)
            print(
                f"Land is Returned Successfully. Fine Charged: Rs {fine}")

    else:
        fine = 0
        extra_duration = 0
        generate_return_invoice(land["kitta_number"], land["customer_name"], land['duration'], extra_duration, land["area"],
                                land["location"], land["direction"], land["price"], fine)
        print("Land is Returned Successfully. No Fine is Charged.")
        rented_lands.remove(land)
        for land in lands_data:
            if land['kitta_number'] == kitta_number:
                land['availability'] = "Available"
        update_availability_in_file(lands_data)


# To validate the number input from the user
def validate_integer_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("Invalid Input. Please enter a valid number.")


#  To validate the name input from the user
def validate_name_input(prompt):
    while True:
        value = input(prompt)
        if not value:
            print("Name cannot be empty.")
        elif not value.replace(" ", "").isalpha():
            print("Name must contain only alphabets.")
        else:
            return value


# find the land by its kitta number.
def find_land_by_kitta_number(kitta_number, lands_data: list[dict]) -> dict:
    """Search for a land by its kitta number."""
    for land in lands_data:
        if land["kitta_number"] == kitta_number:
            return land
    return None

# find the rented land by its kitta number


def find_by_rented_land_kitta_number(rented_land):
    """Find rented land by kitta number."""
    kitta_number = validate_integer_input(
        "Enter Kitta Number: ")
    land = find_land_by_kitta_number(
        kitta_number, rented_land)
    return land


# function to print available lands
def get_available_lands(lands_data: list[dict]):
    """Prints the available lands for rent."""
    print("\n---------------- Available Lands for Rent -----------------\n")
    print("--------------------------------------------------------------")
    print("{:^12} | {:^8} | {:^10} | {:^10} | {:^10}".format(
        "Kitta Number", "Area", "Price", "Location", "Direction"))
    print("--------------------------------------------------------------")
    for land in lands_data:
        if land['availability'].strip() == "Available":
            print("{:^12} | {:^8} | {:^10} | {:^10} | {:^10}".format(
                land['kitta_number'], land['area'], "Rs " + str(land['price']), land['city'], land['direction']))
            print("--------------------------------------------------------------")
    # If no land is available for rent, print a message
    if not any(land['availability'].strip() == "Available" for land in lands_data):
        print("No Land is Available for Rent.")


# function that prints rented land
def get_rented_lands(rented_lands: list[dict]):
    """Print the kitta number and customer name of rented lands"""
    for land in rented_lands:
        print(
            f"Kitta Number: {land['kitta_number']}, Rented To: {land['customer_name']}\n"
        )
    # If no land is rented, print a message
    if not rented_lands:
        print("No Land is Rented.")

# handles rent land operation


def rent_land(lands_data: list[dict], rented_lands: list[dict]):
    global invoice_count
    """ Instructions for renting a land. """
    while True:
        kitta_number = validate_integer_input(
            "Enter Kitta Number: ")
        land = find_land_by_kitta_number(
            kitta_number, lands_data)
        if land:
            if land["availability"].strip() == "Available":
                area = land["area"]
                duration = validate_integer_input(
                    "Enter Duration(Month/s): ")
                customer_name = validate_name_input(
                    "Enter Customer Name: ")

                invoice_number = generate_rental_invoice(
                    kitta_number, customer_name, duration, area, land["city"], land["direction"], land["price"], rented_lands)

                rented_lands.append(
                    add_rented_land_to_file(
                        invoice_number, kitta_number, customer_name, duration, area, land)
                )

                land["availability"] = "Not Available"
                update_availability_in_file(lands_data)
                print("Land is Rented Successfully to ",
                      customer_name, "for ", duration, "month/s")
                break
            elif land["availability"].strip() == "Not Available":
                print("Land is not available for rent.")
                break
        else:
            print("Enter valid Kitta Number to rent land.")

# handles return land operation


def return_land(rented_lands: list[dict], lands_data: list[dict]):
    """ Instructions for returning a land. """
    global return_invoice_count
    while True:
        invoice_number = validate_integer_input(
            "Enter Invoice Number: ")
        rented_land = [
            land for land in rented_lands if land["invoice_number"] == invoice_number]

        if rented_land:
            print(f"\nThe Entered Invoice Number has the following details:\n")
            for land in rented_land:
                print(
                    f"Kitta Number: {land['kitta_number']}\n"
                    f"Rented on: {land['date']}\n"
                    f"Rented To: {land['customer_name']}\n"
                    f"Duration: {land['duration']} Month/s\n"
                    f"Location: {land['location']}\n"
                    f"Area: {land['area']}\n"
                    f"Price: {land['price']}\n"
                )
            while True:
                land = find_by_rented_land_kitta_number(rented_land)

                if land:
                    print(f"\nSelected Land: {land['kitta_number']}")
                    print(
                        f"Rented on: {land['date']}\n"
                        f"Rented To: {land['customer_name']}\n"
                        f"Duration: {land['duration']} Month/s\n"
                        f"Location: {land['location']}\n"
                        f"Area: {land['area']}\n"
                        f"Price: {land['price']}\n"
                    )
                    while True:
                        is_return = input(
                            "Do you want to continue return the land? (y/n): ")
                        if is_return.lower() == 'y':
                            duration_of_rent = round(
                                calculate_duration(land["date"]), 1)
                            handle_return_scenarios(land['kitta_number'],
                                                    land, duration_of_rent, lands_data, rented_lands)
                            return
                        elif is_return.lower() == 'n':
                            print("Land Return Request Cancelled.")
                            return
                        else:
                            print("Invalid Input. Please try again.")
                            continue
                else:  # if land is not found
                    print("Enter valid Kitta Number to return land.")
                    continue
        else:
            print(
                "No land rented with the given invoice number. Enter Correct Invoice Number.")
