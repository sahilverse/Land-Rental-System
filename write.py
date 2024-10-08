# Description: This Module contains the functions to write data to the file.
from datetime import datetime
now = datetime.now()

# Function to update the availability of the land in the file.


def update_availability_in_file(lands_data: list[dict]):
    with open("lands.txt", 'w') as file:
        for land in lands_data:
            file.write(
                f"{land['kitta_number']}, {land['city']}, {land['direction']}, {land['area']}, {land['price']}, {land['availability']}\n")


# Function to write the rented land data to the file.
def add_rented_land_to_file(invoice_number, kitta_number, customer_name, duration, area, land: list[dict]) -> dict:

    rented_lands = {
        "date": now.date().strftime('%d-%m-%Y'),
        "invoice_number": int(invoice_number),
        "kitta_number": int(kitta_number),
        "customer_name": customer_name,
        "duration": int(duration),
        "location": land['city'],
        "area": area,
        "direction": land["direction"],
        "price": int(land['price']),
        "total_price": int(land['price'] * duration)
    }

    with open("rented_lands.txt", 'a') as file:
        file.write(
            f"Date: {now.date().strftime('%d-%m-%Y')}, Invoice Number: {invoice_number}, Kitta Number: {kitta_number}, Customer Name: {customer_name}, Duration: {duration} Month/s, Location: {land['city']}, Area: {area}, price: {land['price']}, total: {land['price'] * duration} \n")

    return rented_lands


# function to create the invoice for the rented land.
def create_rental_receipt(invoice_number, kitta_number, customer_name, duration, area, city, direction, price, total):
    invoice_content = (
        f"\n----------------------- Land Rent Invoice -----------------------\n\n"
        f"Date: {now.date().strftime('%d-%m-%Y')}\t\t\t\t\t Time: {now.time().strftime('%H:%M:%S')}\n\n"
        f"Invoice Number: {invoice_number}\n\n"
        f"Kitta Number: {kitta_number}\t\t\t\t"
        f"Customer Name: {customer_name}\n"
        f"Duration: {duration} Month/s\t\t\t\t"
        f"Location: {city}\n"
        f"Area: {area} Anna\t\t\t\t\t"
        f"Direction: {direction}\n\n"
        f"Price: Rs {price}\n\n"
        f"--------------------------------------------------------------\n\n"
        f"Grand Total:  Rs {total}\n\n"
        f"--------------------------------------------------------------\n\n"
    )
# prints the invoice content.
    print(invoice_content)
    print("Invoice Created Successfully.")
    # creates file with the invoice content.
    with open(f"invoice_{invoice_number}.txt", 'a') as file:
        file.write(invoice_content)


# fubction to create the return invoice for the rented land.


def create_return_receipt(return_invoice_number, kitta_number, customer_name, duration, extra_duration, area, city, direction, price, fine):
    return_invoice_content = (
        f"\n----------------------- Land Return Invoice -----------------------\n\n"
        f"Date: {now.date().strftime('%d-%m-%Y')}\t\t\t\t\t Time: {now.time().strftime('%H:%M:%S')}\n\n"
        f"Return Invoice Number: {return_invoice_number}\n\n"
        f"Kitta Number: {kitta_number}\t\t\t\t\t"
        f"Customer Name: {customer_name}\n"
        f"Duration: {duration} Month/s\t\t\t\t"
        f"Location: {city}\n"
        f"Area: {area} Anna\t\t\t\t\t"
        f"Direction: {direction}\n\n"
        f"Price: Rs {price}\n\n"
        f"Extra Duration: {extra_duration} Month/s\n"
        f"--------------------------------------------------------------\n\n"
        f"Total Fine: Rs {fine}\n"
        f"Note: If contract is not renewed, fine of Rs 500 per month is charged.\n\n"
        f"--------------------------------------------------------------\n\n"
    )

    # Printing return invoice details on the shell
    print(return_invoice_content)
    print("Return Invoice Created Successfully.")

    # Writing return invoice details to a file
    with open(f"return_invoice_{return_invoice_number}.txt", 'a') as file:
        file.write(return_invoice_content)
