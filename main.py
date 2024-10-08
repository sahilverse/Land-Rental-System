from read import read_lands_data
from operations import get_available_lands, get_rented_lands, rent_land, return_land

# Initialize the variables
lands_data = read_lands_data("lands.txt")
rented_lands = []

# Entry Point for the Sytstem


def main():
    """ Main function to start the Land Rental System. """
    while True:
        print("\n-------------- Welcome to the TechnoPropertyNepal -------------\n")
        user_input = input(
            "Enter a number to perform the operation: \n1. Rent Land\n2. Return Land\n3. Get Available Lands\n4. Get Rented Lands\n5. Exit\n\nEnter your choice: ")
        match user_input:
            case "1":
                rent_land(lands_data, rented_lands)
            case "2":
                return_land(rented_lands, lands_data)
            case "3":
                get_available_lands(lands_data)
            case "4":
                get_rented_lands(rented_lands)
            case "5":
                print("Thank you for using the Land Rental System.")
                exit()
            case _:
                print("Invalid Input. Please try again.\n")


# main function to start the land rental system
if __name__ == "__main__":
    while True:
        main()
